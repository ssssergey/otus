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

RANKS_STR = 'AKQJT98765432'


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
    suits = [suit for rank, suit in hand]
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


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    hand5_combinations = combinations(hand, 5)
    best = max(hand5_combinations, key=hand_rank)
    return best


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    common_list = []
    jokers_list = []
    for card in hand:
        if not '?' in card:
            common_list.append(card)
        else:
            jokers_list.append(card)

    # Находим комбинации для карт без джокера
    element_length = 5 - len(jokers_list)
    handx_combinations = list(combinations(common_list, element_length))

    # Увеличиваем длину комбинаций на 1 для каждого джокера
    for joker in jokers_list:
        # Находим все варианты карт для данного джокера
        if 'R' in joker:
            color_suits = ['H', 'D']
        else:
            color_suits = ['S', 'C']
        cards_product = list(product(list(RANKS_STR), color_suits))
        joker_cards = [''.join(item) for item in cards_product]
        # Получаем произведение неполных комбинаций и вариантов карт джокера
        new_element_length = element_length + 1
        result = (handx_combinations, tuple(joker_cards))
        handx_combinations = [item[0] + (item[1],) for item in product(*result)]
        # Оставляем только наборы без повторений
        handx_combinations = [comb for comb in handx_combinations if len(set(comb)) == new_element_length]
        element_length = new_element_length

    best = max(handx_combinations, key=hand_rank)
    return best


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
