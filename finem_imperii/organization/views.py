import json

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse
from django.views.decorators.http import require_POST
from django.views.generic.base import View

from decorators import inchar_required
from organization.models import Organization, PolicyDocument, Capability, CapabilityProposal, CapabilityVote, \
    PositionCandidate
from world.models import Character


@inchar_required
def organization_view(request, organization_id):
    organization = get_object_or_404(Organization, id=organization_id)
    context = {
        'organization': organization,
        'hero_is_member': organization.character_is_member(request.hero),
        'can_use_capabilities': organization.character_can_use_capabilities(request.hero),
    }
    return render(request, 'organization/view_organization.html', context)


def capability_required_decorator(func):
    def inner(*args, **kwargs):
        def fail_the_request(*args, **kwargs):
            messages.error(args[0], "You cannot do that", "danger")
            return redirect(args[0].META.get('HTTP_REFERER', reverse('world:character_home')))
        capability_id = kwargs.get('capability_id')
        if capability_id is None:
            capability_id = args[0].GET.get('capability_id')
        if capability_id is None:
            capability_id = args[0].POST.get('capability_id')
        capability = get_object_or_404(Capability, id=capability_id)
        if not capability.organization.character_can_use_capabilities(args[0].hero):
            return fail_the_request(*args, **kwargs)
        return func(*args, **kwargs)
    return inner


@inchar_required
def document_view(request, document_id):
    document = get_object_or_404(PolicyDocument, id=document_id)
    hero_is_member = document.organization.character_is_member(request.hero)

    if not document.public and not hero_is_member:
        messages.error(request, "You cannot view this document", "danger")
        return redirect(request.META.get('HTTP_REFERER', reverse('world:character_home')))

    context = {
        'document': document,
        'hero_is_member': hero_is_member,
    }
    return render(request, 'organization/view_document.html', context)


@inchar_required
@capability_required_decorator
def capability_view(request, capability_id):
    capability = get_object_or_404(Capability, id=capability_id)
    if not capability.organization.character_can_use_capabilities(request.hero):
        messages.error(request, "You cannot do that", "danger")
        return redirect(request.META.get('HTTP_REFERER', reverse('world:character_home')))

    context = {
        'capability': capability,
        'subtemplate': 'organization/capabilities/{}.html'.format(capability.type),
    }

    if capability.type == Capability.CANDIDACY:
        context['heros_candidacy'] = None
        if capability.applying_to.current_election:
            try:
                context['heros_candidacy'] = capability.applying_to.current_election.positioncandidate_set.get(candidate=request.hero)
            except PositionCandidate.DoesNotExist:
                pass

    return render(request, 'organization/capability.html', context)


@require_POST
@inchar_required
@capability_required_decorator
def election_convoke_view(request, capability_id):
    capability = get_object_or_404(Capability, id=capability_id)

    months_to_election = int(request.POST.get('months_to_election'))
    if not 6 <= months_to_election <= 16:
        messages.error(request, "The time period must be between 6 and 18 months", "danger")
        return redirect(capability.get_absolute_url())

    proposal = {'months_to_election': months_to_election}

    capability.create_proposal(request.hero, proposal)

    if capability.organization.decision_taking == Organization.DEMOCRATIC:
        messages.success(request, "A vote has been started regarding your action", "success")
    else:
        messages.success(request, "Done!", "success")
    return redirect(capability.organization.get_absolute_url())


@require_POST
@inchar_required
@capability_required_decorator
def candidacy_view(request, capability_id):
    capability = get_object_or_404(Capability, id=capability_id)

    election = capability.applying_to.current_election
    if not election:
        messages.error(request, "There is currently no election in progress!", "danger")
        return redirect(capability.get_absolute_url())

    description = request.POST.get('description')
    delete = request.POST.get('delete')

    candidacy, new = PositionCandidate.objects.get_or_create(
        election=election,
        candidate=request.hero
    )

    if delete:
        candidacy.delete()
        messages.success(request, "Your candidacy has been deleted.", "success")
    else:
        candidacy.description = description
        candidacy.save()
        if new:
            messages.success(request, "Your candidacy has been created.", "success")
        else:
            messages.success(request, "Your candidacy has been updated.", "success")

    return redirect(capability.get_absolute_url())


@require_POST
@inchar_required
@capability_required_decorator
def banning_view(request, capability_id):
    capability = get_object_or_404(Capability, id=capability_id, type=Capability.BAN)

    character_to_ban = get_object_or_404(Character, id=request.POST.get('character_to_ban_id'))
    if character_to_ban not in capability.applying_to.character_members.all():
        messages.error(request, "You cannot do that", "danger")
        return redirect(request.META.get('HTTP_REFERER', reverse('world:character_home')))

    proposal = {'character_id': character_to_ban.id}

    capability.create_proposal(request.hero, proposal)

    if capability.organization.decision_taking == Organization.DEMOCRATIC:
        messages.success(request, "A vote has been started regarding your action", "success")
    else:
        messages.success(request, "Done!", "success")
    return redirect(capability.organization.get_absolute_url())


class DocumentCapabilityView(View):
    def get(self, request, capability_id, document_id=None):
        capability = get_object_or_404(Capability, id=capability_id, type=Capability.POLICY_DOCUMENT)
        if document_id is None:
            document = PolicyDocument(organization=capability.applying_to)
            new_document = True
        else:
            document = get_object_or_404(PolicyDocument, id=document_id)
            new_document = False

        context = {
            'capability': capability,
            'document': document,
            'new_document': new_document,
            'subtemplate': 'organization/capabilities/document.html',
        }
        return render(request, 'organization/capability.html', context)

    def post(self, request, capability_id, document_id=None):
        if 'delete' in request.POST.keys() and document_id is None:
            messages.error(request, "You cannot do that", "danger")
            return redirect(request.META.get('HTTP_REFERER', reverse('world:character_home')))

        capability = get_object_or_404(Capability, id=capability_id, type=Capability.POLICY_DOCUMENT)
        if document_id is None:
            new_document = True
        else:
            document = get_object_or_404(PolicyDocument, id=document_id)
            new_document = False

        proposal = {
            'new': new_document,
            'document_id': document.id,
            'delete': 'delete' in request.POST.keys(),
            'title': request.POST.get('title'),
            'body': request.POST.get('body'),
            'public': request.POST.get('public'),
        }

        capability.create_proposal(request.hero, proposal)

        if capability.organization.decision_taking == Organization.DEMOCRATIC:
            messages.success(request, "A vote has been started regarding your action", "success")
        else:
            messages.success(request, "Done!", "success")
        return redirect(capability.organization.get_absolute_url())


class ProposalView(View):
    def check(self, request, proposal_id):
        proposal = get_object_or_404(CapabilityProposal, id=proposal_id)
        if not proposal.capability.organization.character_is_member(request.hero):
            messages.error(request, "You cannot do that", "danger")
            return redirect(request.META.get('HTTP_REFERER', reverse('world:character_home')))

    def get(self, request, proposal_id):
        check_result = self.check(request, proposal_id)
        if check_result is not None:
            return check_result

        proposal = get_object_or_404(CapabilityProposal, id=proposal_id)
        proposal_content = json.loads(proposal.proposal_json)

        try:
            heros_vote = proposal.capabilityvote_set.get(voter=request.hero)
        except CapabilityVote.DoesNotExist:
            heros_vote = None

        context = {
            'proposal': proposal,
            'proposal_content': proposal_content,
            'heros_vote': heros_vote,
            'subtemplate': 'organization/proposals/{}.html'.format(proposal.capability.type),
        }

        if proposal.capability.type == Capability.POLICY_DOCUMENT:
            try:
                context['document'] = PolicyDocument.objects.get(id=proposal_content['document_id'])
            except PolicyDocument.DoesNotExist:
                context['document'] = None

        elif proposal.capability.type == Capability.BAN:
            context['character_to_ban'] = Character.objects.get(id=proposal_content['character_id'])

        return render(request, 'organization/proposal.html', context)

    def post(self, request, proposal_id):
        check_result = self.check(request, proposal_id)
        if check_result is not None:
            return check_result

        proposal = get_object_or_404(CapabilityProposal, id=proposal_id)

        if proposal.closed:
            messages.error(request, "Voting closed", "danger")
            return redirect(request.META.get('HTTP_REFERER', reverse('world:character_home')))

        issued_vote = request.POST.get('vote')
        if issued_vote not in dict(CapabilityVote.VOTE_CHOICES).keys():
            messages.error(request, "Invalid vote", "danger")
            return redirect(request.META.get('HTTP_REFERER', reverse('world:character_home')))

        proposal.issue_vote(request.hero, issued_vote)

        messages.success(request, "Your vote has been issued.", "success")

        return redirect(proposal.get_absolute_url())
