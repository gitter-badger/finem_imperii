from django.test import TestCase

from battle.models import Battle, BattleCharacter, BattleUnit, BattleContubernium, BattleSoldier, BattleOrganization
from organization.models import Organization
from world.initialization import initialize_unit
from world.models import Tile, WorldUnit, NPC


class TestBattleStart(TestCase):
    fixtures = ['simple_world']

    def test_battle_create_from_conflict(self):
        initialize_unit(WorldUnit.objects.get(id=1))
        initialize_unit(WorldUnit.objects.get(id=2))
        tile = Tile.objects.get(id=108)
        battle = Battle.objects.create(tile=tile)
        battle.initialize_from_conflict([Organization.objects.get(id=105), Organization.objects.get(id=112)], tile)

        self.assertEqual(battle.battleside_set.count(), 2)

        self.assertTrue(BattleOrganization.objects.filter(side__battle=battle, organization=Organization.objects.get(id=105)).exists())
        self.assertTrue(BattleOrganization.objects.filter(side__battle=battle, organization=Organization.objects.get(id=112)).exists())
        self.assertEqual(BattleOrganization.objects.count(), 2)

        self.assertTrue(
            BattleOrganization.objects.get(organization_id=105).side.z !=
            BattleOrganization.objects.get(organization_id=112).side.z
        )

        self.assertTrue(BattleCharacter.objects.exists())
        self.assertTrue(BattleCharacter.objects.filter(
            battle_organization__organization=Organization.objects.get(id=105),
        ).exists())
        self.assertTrue(BattleCharacter.objects.filter(
            battle_organization__organization=Organization.objects.get(id=112),
        ).exists())
        self.assertEqual(BattleCharacter.objects.count(), 2)

        self.assertTrue(BattleUnit.objects.exists())
        self.assertTrue(
            BattleUnit.objects.filter(world_unit=WorldUnit.objects.get(id=1), starting_manpower=30).exists()
        )
        self.assertTrue(
            BattleUnit.objects.filter(world_unit=WorldUnit.objects.get(id=2), starting_manpower=30).exists()
        )
        self.assertEqual(BattleUnit.objects.count(), 2)

    def test_start_battle(self):
        initialize_unit(WorldUnit.objects.get(id=1))
        initialize_unit(WorldUnit.objects.get(id=2))
        tile = Tile.objects.get(id=108)
        battle = Battle.objects.create(tile=tile)
        battle.initialize_from_conflict([Organization.objects.get(id=105), Organization.objects.get(id=112)], tile)
        battle.start_battle()

        self.assertTrue(BattleContubernium.objects.exists())
        self.assertEqual(BattleContubernium.objects.count(), 8)
        self.assertTrue(BattleSoldier.objects.exists())
        self.assertEqual(BattleSoldier.objects.count(), 60)

        for npc in NPC.objects.all():
            self.assertTrue(BattleSoldier.objects.filter(world_npc=npc).exists())