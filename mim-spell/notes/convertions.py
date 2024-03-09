import os
import logging

totalBorrow = {
    #'elastic': 248851131868470167457568,  # 248_851,131868470167457568
    #'elastic':   8851131868470167457568,  #   8_851,131868470167457568
    #'base':    232357690628520295106240,  # 232_357,690628520295106240
    #'elastic': 8851.13,
    #'base':  232357.69
    'elastic': 1,
    'base':  100000,
}


def require(condition, message=''):
    if not condition:
        logging.error(f'revert: {message}')
        exit(1)


def toElastic(base, roundUp):
    # totalBorrow.elastic => totalBorrow.base
    # x elastic => base
    # x = base * totalBorrow.elastic / totalBorrow.base
    if totalBorrow['base'] == 0:
        elastic = base
    else:
        elastic = (base * totalBorrow['elastic']) // totalBorrow['base']
        logging.info(f' - toElastic({base}, {roundUp}) => ({base} * {totalBorrow["elastic"]}) / {totalBorrow["base"]} => {elastic}')
        shouldRoundUp = (elastic * totalBorrow['base']) // totalBorrow['elastic'] < base
        if roundUp:
            logging.info(f'   - roundUp: ({elastic} * {totalBorrow["base"]}) / {totalBorrow["elastic"]} < {base} => {shouldRoundUp}')
        if roundUp and shouldRoundUp:
            elastic += 1
        logging.info(f' - return => {elastic}')
    return elastic


def toBase(elastic, roundUp):
    # totalBorrow.elastic => totalBorrow.base
    # elastic             => x base
    # x = (elastic * totalBorrow.base) / totalBorrow.elastic
    if totalBorrow['elastic'] == 0:
        base = elastic
    else:
        base = (elastic * totalBorrow['base']) // totalBorrow['elastic']
        shouldRoundUp = (base * totalBorrow['elastic'] // totalBorrow['base']) < elastic
        logging.info(f' - toBase({elastic}, {roundUp}) => ({elastic} * {totalBorrow["base"]}) / {totalBorrow["elastic"]} => {base}')
        if roundUp:
            logging.info(f'   - roundUp: ({base} * {totalBorrow["elastic"]}) / {totalBorrow["base"]} < {elastic} => {shouldRoundUp}')
        if roundUp and shouldRoundUp:
            base += 1
        logging.info(f' - return => {base}')
    return base


def borrow(elasticAmount):
    logging.info(f'\nborrow({elasticAmount})  totalBorrow: {totalBorrow}')
    base = toBase(elasticAmount, True)
    totalBorrow['elastic'] += elasticAmount
    totalBorrow['base'] += base
    logging.info(f'totalBorrow => {totalBorrow}')


def repay(baseAmount):
    logging.info(f'\nrepay({baseAmount})  totalBorrow: {totalBorrow}')
    require(baseAmount >= 100000, 'minimum repayment not enough')
    elastic = toElastic(baseAmount, True)

    totalBorrow['elastic'] -= elastic
    totalBorrow['base'] -= baseAmount
    require(totalBorrow['elastic'] >= 0 and totalBorrow['base'] >= 0, 'negative values not allowed')
    logging.info(f'totalBorrow => {totalBorrow}')


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

#logging.info(f'initial => {totalBorrow}')
#repay(206_100e18)

borrow(1)
repay(100000)

#for i in range(10):
#    borrow(1)
#    repay(1000)