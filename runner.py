from scrapy.cmdline import execute

try:
    execute(
        [
        'scrapy',
        'crawl',
        'coursesu'
    ]
    )
except SystemExit:
    pass