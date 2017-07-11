#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета. Черный джокер '?B' может быть
# использован в качестве треф или пик любого ранга, красный
# джокер '?R' - в качестве черв и бубен люього ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertoolsю
# Можно свободно определять свои функции и т.п.
# -----------------
from collections import Counter
from itertools import combinations, product

sort_mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
                'A': 14}

ranks_str = 'AKQJT98765432'


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов, отсортированный от большего к меньшему"""
    ranks = [sort_mapping[i[0]] for i in hand]
    ranks.sort(reverse=True)
    return ranks


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    suits = [i[1] for i in hand]
    return len(set(suits)) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    first_rank_index = 0
    while first_rank_index < 4:
        if ranks[first_rank_index] - ranks[first_rank_index + 1] != 1:
            return False
        first_rank_index += 1
    return True


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    counted = Counter(ranks)
    pairs = [rank for rank, amount in counted.items() if amount == 2]
    if len(pairs) == 2:
        return pairs[0], pairs[1]
    else:
        return


def combinations_handler(combinations):
    best = {'rank': 0, 'params': None, 'cards': None}
    for hand5 in combinations:
        rank = hand_rank(hand5)
        rank = {'rank': rank[0], 'params': rank[1:], 'cards': hand5}
        if rank['rank'] > best['rank']:
            best = rank
        elif rank['rank'] == best['rank']:
            best = max([rank, best], key=lambda x: x['params'])
    return best


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    hand5_combinations = combinations(hand, 5)
    best = combinations_handler(hand5_combinations)
    return best['cards']


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    common_list = [card for card in hand if not '?' in card]
    jokers_number = len(hand) - len(common_list)
    handx_combinations = list(combinations(common_list, 5 - jokers_number))
    hand5_combinations = list(combinations(common_list, 5))
    joker_list = set()
    for card in hand:
        if '?' in card:
            if 'R' in card:
                color_suits = ['H', 'D']
            else:
                color_suits = ['S', 'C']
            cards_product = list(product(list(ranks_str), color_suits))
            extra__cards = {''.join(item) for item in cards_product}
            joker_list.update(extra__cards)
    result = (handx_combinations, tuple(joker_list))
    joker_product = list(product(*result))
    joker_combinations = [item[0] + (item[1],) for item in joker_product]
    print joker_combinations
    best = combinations_handler(joker_combinations + hand5_combinations)
    # best = combinations_handler([('7C', 'TC', 'TD', 'TH', 'TS'),])
    print best
    return best['cards']


def test_best_hand():
    print "test_best_hand..."
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'test_best_hand passes'
    print 'OK'


def test_best_wild_hand():
    print "test_best_wild_hand..."
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print 'OK'


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()