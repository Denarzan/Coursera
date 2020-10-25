from abc import ABC, abstractmethod


class Hero:
    """
    Given class.
    """
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):

    def __init__(self, base):
        super().__init__()
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        return self.positive_effects

    @abstractmethod
    def get_negative_effects(self):
        return self.negative_effects

    @abstractmethod
    def get_stats(self):
        return self.stats


class AbstractPositive(AbstractEffect):

    @abstractmethod
    def get_positive_effects(self):
        return self.base.positive_effects.copy()

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        return self.base.stats.copy()


class AbstractNegative(AbstractEffect):

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        return self.base.negative_effects.copy()

    @abstractmethod
    def get_stats(self):
        return self.base.stats.copy()


class Berserk(AbstractPositive):
    def __init__(self, base):
        super().__init__(base)

    def get_positive_effects(self):
        positive_effect = self.base.get_positive_effects()
        positive_effect.append('Berserk')
        return positive_effect

    def get_stats(self):
        hero_stats = self.base.get_stats()
        hero_stats["Strength"] += 7
        hero_stats["Endurance"] += 7
        hero_stats["Agility"] += 7
        hero_stats["Luck"] += 7
        hero_stats["Perception"] -= 3
        hero_stats["Charisma"] -= 3
        hero_stats["Intelligence"] -= 3
        hero_stats["HP"] += 50
        return hero_stats


class Blessing(AbstractPositive):
    def __init__(self, base):
        super().__init__(base)

    def get_positive_effects(self):
        positive_effect = self.base.get_positive_effects()
        positive_effect.append('Blessing')
        return positive_effect

    def get_stats(self):
        hero_stats = self.base.get_stats()
        hero_stats["Strength"] += 2
        hero_stats["Endurance"] += 2
        hero_stats["Agility"] += 2
        hero_stats["Luck"] += 2
        hero_stats["Perception"] += 2
        hero_stats["Charisma"] += 2
        hero_stats["Intelligence"] += 2
        return hero_stats


class Weakness(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)

    def get_negative_effects(self):
        negative_effect = self.base.get_negative_effects()
        negative_effect.append('Weakness')
        return negative_effect

    def get_stats(self):
        hero_stats = self.base.get_stats()
        hero_stats["Strength"] -= 4
        hero_stats["Endurance"] -= 4
        hero_stats["Agility"] -= 4
        return hero_stats


class EvilEye(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)

    def get_negative_effects(self):
        negative_effect = self.base.get_negative_effects()
        negative_effect.append('EvilEye')
        return negative_effect

    def get_stats(self):
        hero_stats = self.base.get_stats()
        hero_stats["Luck"] -= 10
        return hero_stats


class Curse(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)

    def get_negative_effects(self):
        negative_effect = self.base.get_negative_effects()
        negative_effect.append('Curse')
        return negative_effect

    def get_stats(self):
        hero_stats = self.base.get_stats()
        hero_stats["Strength"] -= 2
        hero_stats["Endurance"] -= 2
        hero_stats["Agility"] -= 2
        hero_stats["Luck"] -= 2
        hero_stats["Perception"] -= 2
        hero_stats["Charisma"] -= 2
        hero_stats["Intelligence"] -= 2
        return hero_stats


hero = Hero()
print(hero.get_stats())
print(hero.get_negative_effects())
print(hero.get_positive_effects())
berserk = Berserk(hero)
print(berserk.get_stats())
print(berserk.get_negative_effects())
print(berserk.get_positive_effects())
berserk1 = Berserk(berserk)
print(berserk1.get_stats())
print(berserk1.get_negative_effects())
print(berserk1.get_positive_effects())
blessing = Blessing(berserk1)
print(blessing.get_stats())
print(blessing.get_negative_effects())
print(blessing.get_positive_effects())
blessing.base = blessing.base.base
print(blessing.get_stats())
print(blessing.get_negative_effects())
print(blessing.get_positive_effects())
curse = Curse(blessing)
print(curse.get_stats())
print(curse.get_negative_effects())
print(curse.get_positive_effects())
evileye = EvilEye(curse)
print(evileye.get_stats())
print(evileye.get_negative_effects())
print(evileye.get_positive_effects())
evileye = evileye.base.base.base.base
print(evileye.get_stats())
print(evileye.get_negative_effects())
print(evileye.get_positive_effects())
