import re
import math
import logging
import six.moves
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s: %(message)s', level=logging.INFO)

capabilities_re = re.compile(r'(?:\w+) to ([\w, ]*)(?:; )?')
line_re = re.compile(r'(\d+) units each with (\d+) hit points (\(.*\)\s+)?'
                     r'with an attack that does (\d+) (\w+) damage at initiative (\d+)')

Attr = namedtuple('Attr', 'hits, attack, attack_type, initiative, weaknesses, immunities')


class Group(Attr):
    def __new__(cls, *args):
        u, h, a, t, init, w, imm = args
        self = super(Group, cls).__new__(cls, int(h), int(a), t, int(init), w, imm)
        self.units = int(u)
        return self

    def boost(self, v):
        return Group(self.units, self.hits, self.attack + v, self.attack_type,
                     self.initiative, self.weaknesses, self.immunities)

    @property
    def power(self):
        return self.units * self.attack

    def __repr__(self):
        r = super(Group, self).__repr__()
        return r \
            .replace('Attr(', 'Group(units=%d, ' % self.units) \
            .replace(')', ', power=%d)' % self.power)

    def take_damage(self, attacker):
        d, _, __ = self.damage_by(attacker)
        killed = min(self.units, d // self.hits)
        self.units -= killed
        return killed

    def damage_by(self, attacker):
        if attacker.attack_type in self.weaknesses:
            d = attacker.power * 2
        elif attacker.attack_type in self.immunities:
            d = 0
        else:
            d = attacker.power
        return d, self.power, self.initiative

    def targeting_order(self):
        return self.power, self.initiative

    def attacking_order(self):
        return self.initiative,


def line_parse(lines):
    for line in lines:
        m = line_re.match(line)
        if m:
            units, hit, caps_opt, attack, attack_type, initiative = m.groups()
            caps = capabilities_re.match(caps_opt[1:-2]) if caps_opt else None
            weaknesses, immunities = [], []
            while caps:
                abilities = [_.strip() for _ in caps.groups()[0].split(',')]
                if 'weak' in caps.group():
                    weaknesses = abilities
                elif 'immune' in caps.group():
                    immunities = abilities
                caps = capabilities_re.match(caps.string[caps.end():])
            yield Group(units, hit, attack, attack_type, initiative, weaknesses, immunities)
        else:
            raise StopIteration


def parse(description):
    it = iter(description)
    lines = six.moves.map(str.strip, it)
    while True:
        sys_name = 'immune' if 'system' in next(lines).lower() else 'infect'
        system = [group for group in line_parse(lines)]
        yield sys_name.replace(':', ''), system


def count_living(systems):
    return {
        name: six.moves.reduce(lambda a, i: a + i.units, sys, 0)
        for name, sys in six.iteritems(systems)
    }


def filter_living(systems):
    return [(k, v) for k, v in six.iteritems(count_living(systems)) if v]


def target(systems):
    for name, system in six.iteritems(systems):
        other = 'immune' if name == 'infect' else 'infect'
        attackers = sorted(
            [(a.targeting_order(), a) for a in system if a.units], reverse=True
        )
        remaining_targets = [t for t in systems[other] if t.units]
        for _, a in attackers:
            available = sorted(
                [(t.damage_by(a), t) for t in remaining_targets], reverse=True
            )
            if available:
                (damage, _, __), t = max(available)
                if damage != 0:
                    remaining_targets.remove(t)
                    yield (a.initiative, t, a)


def fight(systems):
    g1, g2 = count_living(systems).values()
    while g1 and g2:
        prev = g1, g2
        chosen_targets = target(systems)
        for _, targeted, attacker in sorted(chosen_targets, reverse=True):
            targeted.take_damage(attacker)
        g1, g2 = count_living(systems).values()
        if prev == (g1, g2):
            break
    return systems


def test():
    test_txt = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""
    systems = dict(parse(test_txt.strip().split('\n')))
    result = fight(systems)
    name, units = max(filter_living(result))
    assert units == 5216 and 'infect' == name

    systems = dict(parse(test_txt.strip().split('\n')))
    boost(systems, 1570)
    result = fight(systems)
    name, units = max(filter_living(result))
    assert units == 51 and 'immune' == name


def boost(systems, v):
    systems['immune'] = [group.boost(v) for group in systems['immune']]
    return systems


def simulate(boost_value):
    with open('input24.txt') as in_file:
        systems = dict(parse(in_file))

    systems = boost(systems, boost_value)
    result = fight(systems)
    living = filter_living(result)
    if len(living) == 1:
        return max(living)
    return 'tie', None


def main():
    logger.info("Start: ")
    _, units = simulate(0)
    logger.info("Solution #1: %s", units)

    boost_min, boost_max = 1, 100
    cur_boost = boost_max - (boost_max - boost_min) // 2
    sol2 = 'unknown'
    while (boost_max - boost_min) > 1:
        logger.info("Boost between %d-%d: trying %d", boost_min, boost_max, cur_boost)
        winner, units = simulate(cur_boost)
        if winner == 'immune':
            sol2 = units
            boost_max = min(boost_max, cur_boost)
            cur_boost = cur_boost - (cur_boost - boost_min) // 2
        else:
            boost_min = max(boost_min, cur_boost)
            cur_boost = cur_boost + int(math.ceil((float(boost_max) - cur_boost) / 2))

    logger.info("Solution #2: %s", sol2)


if __name__ == '__main__':
    test()
    main()
