#!c:\python27\python.exe

#from numpy import random
import random, time
from threading import Thread
from blinkstick import blinkstick
from flask import Flask, json, request, Response
#from threading import Lock for another day/time

# https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F
named_colors={
    '':{'r':None,'g':None,'b':None},
    'absolute zero':{'r':0,'g':72,'b':186},
    'acid green':{'r':176,'g':191,'b':26},
    'aero':{'r':124,'g':185,'b':232},
    'aero blue':{'r':192,'g':232,'b':213},
    'african violet':{'r':178,'g':132,'b':190},
    'air superiority blue':{'r':114,'g':160,'b':193},
    'alabaster':{'r':237,'g':234,'b':224},
    'alice blue':{'r':240,'g':248,'b':255},
    'alloy orange':{'r':196,'g':98,'b':16},
    'almond':{'r':239,'g':222,'b':205},
    'amaranth':{'r':229,'g':43,'b':80},
    'amaranth pink':{'r':241,'g':156,'b':187},
    'amaranth purple':{'r':171,'g':39,'b':79},
    'amaranth red':{'r':211,'g':33,'b':45},
    'amazon':{'r':59,'g':122,'b':87},
    'amber':{'r':255,'g':191,'b':0},
    'amethyst':{'r':153,'g':102,'b':204},
    'android green':{'r':164,'g':198,'b':57},
    'antique brass':{'r':205,'g':149,'b':117},
    'antique bronze':{'r':102,'g':93,'b':30},
    'antique fuchsia':{'r':145,'g':92,'b':131},
    'antique ruby':{'r':132,'g':27,'b':45},
    'antique white':{'r':250,'g':235,'b':215},
    'ao':{'r':0,'g':128,'b':0},
    'apple green':{'r':141,'g':182,'b':0},
    'apricot':{'r':251,'g':206,'b':177},
    'aqua':{'r':0,'g':255,'b':255},
    'aquamarine':{'r':127,'g':255,'b':212},
    'arctic lime':{'r':208,'g':255,'b':20},
    'army green':{'r':75,'g':83,'b':32},
    'artichoke':{'r':143,'g':151,'b':121},
    'arylide yellow':{'r':233,'g':214,'b':107},
    'ash gray':{'r':178,'g':190,'b':181},
    'asparagus':{'r':135,'g':169,'b':107},
    'atomic tangerine':{'r':255,'g':153,'b':102},
    'auburn':{'r':165,'g':42,'b':42},
    'aureolin':{'r':253,'g':238,'b':0},
    'avocado':{'r':86,'g':130,'b':3},
    'azure':{'r':0,'g':127,'b':255},
    'baby blue':{'r':137,'g':207,'b':240},
    'baby blue eyes':{'r':161,'g':202,'b':241},
    'baby pink':{'r':244,'g':194,'b':194},
    'baby powder':{'r':254,'g':254,'b':250},
    'baker miller pink':{'r':255,'g':145,'b':175},
    'banana mania':{'r':250,'g':231,'b':181},
    'barbie pink':{'r':218,'g':24,'b':132},
    'barn red':{'r':124,'g':10,'b':2},
    'battleship grey':{'r':132,'g':132,'b':130},
    'beau blue':{'r':188,'g':212,'b':230},
    'beaver':{'r':159,'g':129,'b':112},
    'beige':{'r':245,'g':245,'b':220},
    'bedazzled blue':{'r':46,'g':88,'b':148},
    'bisque':{'r':255,'g':228,'b':196},
    'bistre':{'r':61,'g':43,'b':31},
    'bistre brown':{'r':150,'g':113,'b':23},
    'bitter lemon':{'r':202,'g':224,'b':13},
    'bitter lime':{'r':191,'g':255,'b':0},
    'bittersweet':{'r':254,'g':111,'b':94},
    'bittersweet shimmer':{'r':191,'g':79,'b':81},
    'black':{'r':0,'g':0,'b':0},
    'black bean':{'r':61,'g':12,'b':2},
    'black chocolate':{'r':27,'g':24,'b':17},
    'black coffee':{'r':59,'g':47,'b':47},
    'black coral':{'r':84,'g':98,'b':111},
    'black olive':{'r':59,'g':60,'b':54},
    'black shadows':{'r':191,'g':175,'b':178},
    'blanched almond':{'r':255,'g':235,'b':205},
    'blast off bronze':{'r':165,'g':113,'b':100},
    'bleu de france':{'r':49,'g':140,'b':231},
    'blizzard blue':{'r':172,'g':229,'b':238},
    'blond':{'r':250,'g':240,'b':190},
    'blood red':{'r':102,'g':0,'b':0},
    'blue':{'r':0,'g':0,'b':255},
    'blue bell':{'r':162,'g':162,'b':208},
    'blue gray':{'r':102,'g':153,'b':204},
    'blue green':{'r':13,'g':152,'b':186},
    'blue jeans':{'r':93,'g':173,'b':236},
    'blue sapphire':{'r':18,'g':97,'b':128},
    'blue violet':{'r':138,'g':43,'b':226},
    'blue yonder':{'r':80,'g':114,'b':167},
    'bluetiful':{'r':60,'g':105,'b':231},
    'blush':{'r':222,'g':93,'b':131},
    'bole':{'r':121,'g':68,'b':59},
    'bone':{'r':227,'g':218,'b':201},
    'bottle green':{'r':0,'g':106,'b':78},
    'brandy':{'r':135,'g':65,'b':63},
    'brick red':{'r':203,'g':65,'b':84},
    'bright green':{'r':102,'g':255,'b':0},
    'bright lilac':{'r':216,'g':145,'b':239},
    'bright maroon':{'r':195,'g':33,'b':72},
    'bright navy blue':{'r':25,'g':116,'b':210},
    'bright yellow':{'r':255,'g':170,'b':29},
    'brilliant rose':{'r':255,'g':85,'b':163},
    'brink pink':{'r':251,'g':96,'b':127},
    'british racing green':{'r':0,'g':66,'b':37},
    'bronze':{'r':205,'g':127,'b':50},
    'brown':{'r':136,'g':84,'b':11},
    'brown sugar':{'r':175,'g':110,'b':77},
    'brunswick green':{'r':27,'g':77,'b':62},
    'bud green':{'r':123,'g':182,'b':97},
    'buff':{'r':255,'g':198,'b':128},
    'burgundy':{'r':128,'g':0,'b':32},
    'burlywood':{'r':222,'g':184,'b':135},
    'burnished brown':{'r':161,'g':122,'b':116},
    'burnt orange':{'r':204,'g':85,'b':0},
    'burnt sienna':{'r':233,'g':116,'b':81},
    'burnt umber':{'r':138,'g':51,'b':36},
    'byzantine':{'r':189,'g':51,'b':164},
    'byzantium':{'r':112,'g':41,'b':99},
    'cadet':{'r':83,'g':104,'b':114},
    'cadet blue':{'r':95,'g':158,'b':160},
    'cadet grey':{'r':145,'g':163,'b':176},
    'cadmium green':{'r':0,'g':107,'b':60},
    'cadmium orange':{'r':237,'g':135,'b':45},
    'cadmium red':{'r':227,'g':0,'b':34},
    'cadmium yellow':{'r':255,'g':246,'b':0},
    'cambridge blue':{'r':163,'g':193,'b':173},
    'camel':{'r':193,'g':154,'b':107},
    'cameo pink':{'r':239,'g':187,'b':204},
    'canary':{'r':255,'g':255,'b':153},
    'canary yellow':{'r':255,'g':239,'b':0},
    'candy apple red':{'r':255,'g':8,'b':0},
    'candy pink':{'r':228,'g':113,'b':122},
    'capri':{'r':0,'g':191,'b':255},
    'caput mortuum':{'r':89,'g':39,'b':32},
    'cardinal':{'r':196,'g':30,'b':58},
    'caribbean green':{'r':0,'g':204,'b':153},
    'carmine':{'r':150,'g':0,'b':24},
    'carnation pink':{'r':255,'g':166,'b':201},
    'carnelian':{'r':179,'g':27,'b':27},
    'carolina blue':{'r':86,'g':160,'b':211},
    'carrot orange':{'r':237,'g':145,'b':33},
    'castleton green':{'r':0,'g':86,'b':63},
    'catawba':{'r':112,'g':54,'b':66},
    'cedar chest':{'r':201,'g':90,'b':73},
    'celadon':{'r':172,'g':225,'b':175},
    'celadon blue':{'r':0,'g':123,'b':167},
    'celadon green':{'r':47,'g':132,'b':124},
    'celeste':{'r':178,'g':255,'b':255},
    'celtic blue':{'r':36,'g':107,'b':206},
    'cerise':{'r':222,'g':49,'b':99},
    'cerulean':{'r':0,'g':123,'b':167},
    'cerulean blue':{'r':42,'g':82,'b':190},
    'cerulean frost':{'r':109,'g':155,'b':195},
    'cerulean':{'r':29,'g':172,'b':214},
    'cg blue':{'r':0,'g':122,'b':165},
    'cg red':{'r':224,'g':60,'b':49},
    'champagne':{'r':247,'g':231,'b':206},
    'champagne pink':{'r':241,'g':221,'b':207},
    'charcoal':{'r':54,'g':69,'b':79},
    'charleston green':{'r':35,'g':43,'b':43},
    'charm pink':{'r':230,'g':143,'b':172},
    'chartreuse':{'r':223,'g':255,'b':0},
    'cherry blossom pink':{'r':255,'g':183,'b':197},
    'chestnut':{'r':149,'g':69,'b':53},
    'chili red':{'r':226,'g':61,'b':40},
    'china pink':{'r':222,'g':111,'b':161},
    'china rose':{'r':168,'g':81,'b':110},
    'chinese red':{'r':170,'g':56,'b':30},
    'chinese violet':{'r':133,'g':96,'b':136},
    'chinese yellow':{'r':255,'g':178,'b':0},
    'chocolate':{'r':123,'g':63,'b':0},
    'chocolate cosmos':{'r':88,'g':17,'b':26},
    'chrome yellow':{'r':255,'g':167,'b':0},
    'cinereous':{'r':152,'g':129,'b':123},
    'cinnabar':{'r':227,'g':66,'b':52},
    'cinnamon satin':{'r':205,'g':96,'b':126},
    'citrine':{'r':228,'g':208,'b':10},
    'citron':{'r':159,'g':169,'b':31},
    'claret':{'r':127,'g':23,'b':52},
    'cobalt blue':{'r':0,'g':71,'b':171},
    'cocoa brown':{'r':210,'g':105,'b':30},
    'coffee':{'r':111,'g':78,'b':55},
    'columbia blue':{'r':185,'g':217,'b':235},
    'congo pink':{'r':248,'g':131,'b':121},
    'cool grey':{'r':140,'g':146,'b':172},
    'copper':{'r':184,'g':115,'b':51},
    'copper penny':{'r':173,'g':111,'b':105},
    'copper red':{'r':203,'g':109,'b':81},
    'copper rose':{'r':153,'g':102,'b':102},
    'coquelicot':{'r':255,'g':56,'b':0},
    'coral':{'r':255,'g':127,'b':80},
    'coral pink':{'r':248,'g':131,'b':121},
    'cordovan':{'r':137,'g':63,'b':69},
    'corn':{'r':251,'g':236,'b':93},
    'cornell red':{'r':179,'g':27,'b':27},
    'cornflower blue':{'r':100,'g':149,'b':237},
    'cornsilk':{'r':255,'g':248,'b':220},
    'cosmic cobalt':{'r':46,'g':45,'b':136},
    'cosmic latte':{'r':255,'g':248,'b':231},
    'coyote brown':{'r':129,'g':97,'b':60},
    'cotton candy':{'r':255,'g':188,'b':217},
    'cream':{'r':255,'g':253,'b':208},
    'crimson':{'r':220,'g':20,'b':60},
    'crystal':{'r':167,'g':216,'b':222},
    'cultured':{'r':245,'g':245,'b':245},
    'cyan':{'r':0,'g':255,'b':255},
    'cyber grape':{'r':88,'g':66,'b':124},
    'cyber yellow':{'r':255,'g':211,'b':0},
    'cyclamen':{'r':245,'g':111,'b':161},
    'dark blue gray':{'r':102,'g':102,'b':153},
    'dark brown':{'r':101,'g':67,'b':33},
    'dark byzantium':{'r':93,'g':57,'b':84},
    'dark cornflower blue':{'r':38,'g':66,'b':139},
    'dark cyan':{'r':0,'g':139,'b':139},
    'dark electric blue':{'r':83,'g':104,'b':120},
    'dark goldenrod':{'r':184,'g':134,'b':11},
    'dark green':{'r':1,'g':50,'b':32},
    'dark jungle green':{'r':26,'g':36,'b':33},
    'dark khaki':{'r':189,'g':183,'b':107},
    'dark lava':{'r':72,'g':60,'b':50},
    'dark liver':{'r':83,'g':75,'b':79},
    'dark magenta':{'r':139,'g':0,'b':139},
    'dark moss green':{'r':74,'g':93,'b':35},
    'dark olive green':{'r':85,'g':107,'b':47},
    'dark orange':{'r':255,'g':140,'b':0},
    'dark orchid':{'r':153,'g':50,'b':204},
    'dark pastel green':{'r':3,'g':192,'b':60},
    'dark purple':{'r':48,'g':25,'b':52},
    'dark red':{'r':139,'g':0,'b':0},
    'dark salmon':{'r':233,'g':150,'b':122},
    'dark sea green':{'r':143,'g':188,'b':143},
    'dark sienna':{'r':60,'g':20,'b':20},
    'dark sky blue':{'r':140,'g':190,'b':214},
    'dark slate blue':{'r':72,'g':61,'b':139},
    'dark slate gray':{'r':47,'g':79,'b':79},
    'dark spring green':{'r':23,'g':114,'b':69},
    'dark turquoise':{'r':0,'g':206,'b':209},
    'dark violet':{'r':148,'g':0,'b':211},
    'dartmouth green':{'r':0,'g':112,'b':60},
    'davies grey':{'r':85,'g':85,'b':85},
    'deep cerise':{'r':218,'g':50,'b':135},
    'deep champagne':{'r':250,'g':214,'b':165},
    'deep chestnut':{'r':185,'g':78,'b':72},
    'deep jungle green':{'r':0,'g':75,'b':73},
    'deep pink':{'r':255,'g':20,'b':147},
    'deep saffron':{'r':255,'g':153,'b':51},
    'deep sky blue':{'r':0,'g':191,'b':255},
    'deep space sparkle':{'r':74,'g':100,'b':108},
    'deep taupe':{'r':126,'g':94,'b':96},
    'denim':{'r':21,'g':96,'b':189},
    'denim blue':{'r':34,'g':67,'b':182},
    'desert':{'r':193,'g':154,'b':107},
    'desert sand':{'r':237,'g':201,'b':175},
    'dim gray':{'r':105,'g':105,'b':105},
    'dodger blue':{'r':30,'g':144,'b':255},
    'dogwood rose':{'r':215,'g':24,'b':104},
    'drab':{'r':150,'g':113,'b':23},
    'duke blue':{'r':0,'g':0,'b':156},
    'dutch white':{'r':239,'g':223,'b':187},
    'earth yellow':{'r':225,'g':169,'b':95},
    'ebony':{'r':85,'g':93,'b':80},
    'ecru':{'r':194,'g':178,'b':128},
    'eerie black':{'r':27,'g':27,'b':27},
    'eggplant':{'r':97,'g':64,'b':81},
    'eggshell':{'r':240,'g':234,'b':214},
    'egyptian blue':{'r':16,'g':52,'b':166},
    'eigengrau':{'r':22,'g':22,'b':29},
    'electric blue':{'r':125,'g':249,'b':255},
    'electric green':{'r':0,'g':255,'b':0},
    'electric indigo':{'r':111,'g':0,'b':255},
    'electric lime':{'r':204,'g':255,'b':0},
    'electric purple':{'r':191,'g':0,'b':255},
    'electric violet':{'r':143,'g':0,'b':255},
    'emerald':{'r':80,'g':200,'b':120},
    'eminence':{'r':108,'g':48,'b':130},
    'english green':{'r':27,'g':77,'b':62},
    'english lavender':{'r':180,'g':131,'b':149},
    'english red':{'r':171,'g':75,'b':82},
    'english vermillion':{'r':204,'g':71,'b':75},
    'english violet':{'r':86,'g':60,'b':92},
    'erin':{'r':0,'g':255,'b':64},
    'eton blue':{'r':150,'g':200,'b':162},
    'fallow':{'r':193,'g':154,'b':107},
    'falu red':{'r':128,'g':24,'b':24},
    'fandango':{'r':181,'g':51,'b':137},
    'fandango pink':{'r':222,'g':82,'b':133},
    'fashion fuchsia':{'r':244,'g':0,'b':161},
    'fawn':{'r':229,'g':170,'b':112},
    'feldgrau':{'r':77,'g':93,'b':83},
    'fern green':{'r':79,'g':121,'b':66},
    'field drab':{'r':108,'g':84,'b':30},
    'fiery rose':{'r':255,'g':84,'b':112},
    'firebrick':{'r':178,'g':34,'b':34},
    'fire engine red':{'r':206,'g':32,'b':41},
    'fire opal':{'r':233,'g':92,'b':75},
    'flame':{'r':226,'g':88,'b':34},
    'flax':{'r':238,'g':220,'b':130},
    'flirt':{'r':162,'g':0,'b':109},
    'floral white':{'r':255,'g':250,'b':240},
    'fluorescent blue':{'r':21,'g':244,'b':238},
    'forest green':{'r':95,'g':167,'b':119},
    'french beige':{'r':166,'g':123,'b':91},
    'french bistre':{'r':133,'g':109,'b':77},
    'french blue':{'r':0,'g':114,'b':187},
    'french fuchsia':{'r':253,'g':63,'b':146},
    'french lilac':{'r':134,'g':96,'b':142},
    'french lime':{'r':158,'g':253,'b':56},
    'french mauve':{'r':212,'g':115,'b':212},
    'french pink':{'r':253,'g':108,'b':158},
    'french raspberry':{'r':199,'g':44,'b':72},
    'french rose':{'r':246,'g':74,'b':138},
    'french sky blue':{'r':119,'g':181,'b':254},
    'french violet':{'r':136,'g':6,'b':206},
    'frostbite':{'r':233,'g':54,'b':167},
    'fuchsia':{'r':255,'g':0,'b':255},
    'fuchsia purple':{'r':204,'g':57,'b':123},
    'fuchsia rose':{'r':199,'g':67,'b':117},
    'fulvous':{'r':228,'g':132,'b':0},
    'fuzzy wuzzy':{'r':135,'g':66,'b':31},
    'gainsboro':{'r':220,'g':220,'b':220},
    'gamboge':{'r':228,'g':155,'b':15},
    'generic viridian':{'r':0,'g':127,'b':102},
    'ghost white':{'r':248,'g':248,'b':255},
    'glaucous':{'r':96,'g':130,'b':182},
    'glossy grape':{'r':171,'g':146,'b':179},
    'go green':{'r':0,'g':171,'b':102},
    'gold':{'r':165,'g':124,'b':0},
    'gold fusion':{'r':133,'g':117,'b':78},
    'golden brown':{'r':153,'g':101,'b':21},
    'golden poppy':{'r':252,'g':194,'b':0},
    'golden yellow':{'r':255,'g':223,'b':0},
    'goldenrod':{'r':218,'g':165,'b':32},
    'granite gray':{'r':103,'g':103,'b':103},
    'granny smith apple':{'r':168,'g':228,'b':160},
    'gray':{'r':128,'g':128,'b':128},
    'green':{'r':0,'g':255,'b':0},
    'green blue':{'r':17,'g':100,'b':180},
    'green cyan':{'r':0,'g':153,'b':102},
    'green lizard':{'r':167,'g':244,'b':50},
    'green sheen':{'r':110,'g':174,'b':161},
    'green yellow':{'r':173,'g':255,'b':47},
    'grullo':{'r':169,'g':154,'b':134},
    'gunmetal':{'r':42,'g':52,'b':57},
    'han blue':{'r':68,'g':108,'b':207},
    'han purple':{'r':82,'g':24,'b':250},
    'hansa yellow':{'r':233,'g':214,'b':107},
    'harlequin':{'r':63,'g':255,'b':0},
    'harvest gold':{'r':218,'g':145,'b':0},
    'heat wave':{'r':255,'g':122,'b':0},
    'heliotrope':{'r':223,'g':115,'b':255},
    'heliotrope gray':{'r':170,'g':152,'b':169},
    'hollywood cerise':{'r':244,'g':0,'b':161},
    'honeydew':{'r':240,'g':255,'b':240},
    'honolulu blue':{'r':0,'g':109,'b':176},
    'hookers green':{'r':73,'g':121,'b':107},
    'hot magenta':{'r':255,'g':29,'b':206},
    'hot pink':{'r':255,'g':105,'b':180},
    'hunter green':{'r':53,'g':94,'b':59},
    'iceberg':{'r':113,'g':166,'b':210},
    'icterine':{'r':252,'g':247,'b':94},
    'illuminating emerald':{'r':49,'g':145,'b':119},
    'imperial red':{'r':237,'g':41,'b':57},
    'inchworm':{'r':178,'g':236,'b':93},
    'independence':{'r':76,'g':81,'b':109},
    'india green':{'r':19,'g':136,'b':8},
    'indian red':{'r':205,'g':92,'b':92},
    'indian yellow':{'r':227,'g':168,'b':87},
    'indigo':{'r':75,'g':0,'b':130},
    'indigo dye':{'r':0,'g':65,'b':106},
    'international orange':{'r':255,'g':79,'b':0},
    'iris':{'r':90,'g':79,'b':207},
    'irresistible':{'r':179,'g':68,'b':108},
    'isabelline':{'r':244,'g':240,'b':236},
    'italian sky blue':{'r':178,'g':255,'b':255},
    'ivory':{'r':255,'g':255,'b':240},
    'jade':{'r':0,'g':168,'b':107},
    'japanese carmine':{'r':157,'g':41,'b':51},
    'japanese violet':{'r':91,'g':50,'b':86},
    'jasmine':{'r':248,'g':222,'b':126},
    'jazzberry jam':{'r':165,'g':11,'b':94},
    'jet':{'r':52,'g':52,'b':52},
    'jonquil':{'r':244,'g':202,'b':22},
    'june bud':{'r':189,'g':218,'b':87},
    'jungle green':{'r':41,'g':171,'b':135},
    'kelly green':{'r':76,'g':187,'b':23},
    'keppel':{'r':58,'g':176,'b':158},
    'key lime':{'r':232,'g':244,'b':140},
    'khaki':{'r':195,'g':176,'b':145},
    'kobe':{'r':136,'g':45,'b':23},
    'kobi':{'r':231,'g':159,'b':196},
    'kobicha':{'r':107,'g':68,'b':35},
    'kombu green':{'r':53,'g':66,'b':48},
    'ksu purple':{'r':81,'g':40,'b':136},
    'languid lavender':{'r':214,'g':202,'b':221},
    'lapis lazuli':{'r':38,'g':97,'b':156},
    'laser lemon':{'r':255,'g':255,'b':102},
    'laurel green':{'r':169,'g':186,'b':157},
    'lava':{'r':207,'g':16,'b':32},
    'lavender':{'r':181,'g':126,'b':220},
    'lavender blue':{'r':204,'g':204,'b':255},
    'lavender blush':{'r':255,'g':240,'b':245},
    'lavender gray':{'r':196,'g':195,'b':208},
    'lawn green':{'r':124,'g':252,'b':0},
    'lemon':{'r':255,'g':247,'b':0},
    'lemon chiffon':{'r':255,'g':250,'b':205},
    'lemon curry':{'r':204,'g':160,'b':29},
    'lemon glacier':{'r':253,'g':255,'b':0},
    'lemon meringue':{'r':246,'g':234,'b':190},
    'lemon yellow':{'r':255,'g':244,'b':79},
    'liberty':{'r':84,'g':90,'b':167},
    'light blue':{'r':173,'g':216,'b':230},
    'light coral':{'r':240,'g':128,'b':128},
    'light cornflower blue':{'r':147,'g':204,'b':234},
    'light cyan':{'r':224,'g':255,'b':255},
    'light french beige':{'r':200,'g':173,'b':127},
    'light goldenrod yellow':{'r':250,'g':250,'b':210},
    'light gray':{'r':211,'g':211,'b':211},
    'light green':{'r':144,'g':238,'b':144},
    'light orange':{'r':254,'g':216,'b':177},
    'light periwinkle':{'r':197,'g':203,'b':225},
    'light pink':{'r':255,'g':182,'b':193},
    'light salmon':{'r':255,'g':160,'b':122},
    'light sea green':{'r':32,'g':178,'b':170},
    'light sky blue':{'r':135,'g':206,'b':250},
    'light slate gray':{'r':119,'g':136,'b':153},
    'light steel blue':{'r':176,'g':196,'b':222},
    'light yellow':{'r':255,'g':255,'b':224},
    'lilac':{'r':200,'g':162,'b':200},
    'lilac luster':{'r':174,'g':152,'b':170},
    'lime':{'r':191,'g':255,'b':0},
    'lime green':{'r':50,'g':205,'b':50},
    'lincoln green':{'r':25,'g':89,'b':5},
    'linen':{'r':250,'g':240,'b':230},
    'lion':{'r':193,'g':154,'b':107},
    'liseran purple':{'r':222,'g':111,'b':161},
    'little boy blue':{'r':108,'g':160,'b':220},
    'liver':{'r':103,'g':76,'b':71},
    'liver chestnut':{'r':152,'g':116,'b':86},
    'livid':{'r':102,'g':153,'b':204},
    'macaroni and cheese':{'r':255,'g':189,'b':136},
    'madder lake':{'r':204,'g':51,'b':54},
    'magenta':{'r':255,'g':0,'b':255},
    'magenta haze':{'r':159,'g':69,'b':118},
    'magic mint':{'r':170,'g':240,'b':209},
    'magnolia':{'r':242,'g':232,'b':215},
    'mahogany':{'r':192,'g':64,'b':0},
    'maize':{'r':251,'g':236,'b':93},
    'majorelle blue':{'r':96,'g':80,'b':220},
    'malachite':{'r':11,'g':218,'b':81},
    'manatee':{'r':151,'g':154,'b':170},
    'mandarin':{'r':243,'g':122,'b':72},
    'mango':{'r':253,'g':190,'b':2},
    'mango tango':{'r':255,'g':130,'b':67},
    'mantis':{'r':116,'g':195,'b':101},
    'mardi gras':{'r':136,'g':0,'b':133},
    'marigold':{'r':234,'g':162,'b':33},
    'maroon':{'r':195,'g':33,'b':72},
    'mauve':{'r':224,'g':176,'b':255},
    'mauve taupe':{'r':145,'g':95,'b':109},
    'mauvelous':{'r':239,'g':152,'b':170},
    'maximum blue':{'r':71,'g':171,'b':204},
    'maximum blue green':{'r':48,'g':191,'b':191},
    'maximum blue purple':{'r':172,'g':172,'b':230},
    'maximum green':{'r':94,'g':140,'b':49},
    'maximum green yellow':{'r':217,'g':230,'b':80},
    'maximum purple':{'r':115,'g':51,'b':128},
    'maximum red':{'r':217,'g':33,'b':33},
    'maximum red purple':{'r':166,'g':58,'b':121},
    'maximum yellow':{'r':250,'g':250,'b':55},
    'maximum yellow red':{'r':242,'g':186,'b':73},
    'may green':{'r':76,'g':145,'b':65},
    'maya blue':{'r':115,'g':194,'b':251},
    'medium aquamarine':{'r':102,'g':221,'b':170},
    'medium blue':{'r':0,'g':0,'b':205},
    'medium candy apple red':{'r':226,'g':6,'b':44},
    'medium carmine':{'r':175,'g':64,'b':53},
    'medium champagne':{'r':243,'g':229,'b':171},
    'medium orchid':{'r':186,'g':85,'b':211},
    'medium purple':{'r':147,'g':112,'b':219},
    'medium sea green':{'r':60,'g':179,'b':113},
    'medium slate blue':{'r':123,'g':104,'b':238},
    'medium spring green':{'r':0,'g':250,'b':154},
    'medium turquoise':{'r':72,'g':209,'b':204},
    'medium violet red':{'r':199,'g':21,'b':133},
    'mellow apricot':{'r':248,'g':184,'b':120},
    'mellow yellow':{'r':248,'g':222,'b':126},
    'melon':{'r':254,'g':186,'b':173},
    'metallic gold':{'r':211,'g':175,'b':55},
    'metallic seaweed':{'r':10,'g':126,'b':140},
    'metallic sunburst':{'r':156,'g':124,'b':56},
    'mexican pink':{'r':228,'g':0,'b':124},
    'middle blue':{'r':126,'g':212,'b':230},
    'middle blue green':{'r':141,'g':217,'b':204},
    'middle blue purple':{'r':139,'g':114,'b':190},
    'middle grey':{'r':139,'g':134,'b':128},
    'middle green':{'r':77,'g':140,'b':87},
    'middle green yellow':{'r':172,'g':191,'b':96},
    'middle purple':{'r':217,'g':130,'b':181},
    'middle red':{'r':229,'g':142,'b':115},
    'middle red purple':{'r':165,'g':83,'b':83},
    'middle yellow':{'r':255,'g':235,'b':0},
    'middle yellow red':{'r':236,'g':177,'b':118},
    'midnight':{'r':112,'g':38,'b':112},
    'midnight blue':{'r':25,'g':25,'b':112},
    'midnight green':{'r':0,'g':73,'b':83},
    'mikado yellow':{'r':255,'g':196,'b':12},
    'mimi pink':{'r':255,'g':218,'b':233},
    'mindaro':{'r':227,'g':249,'b':136},
    'ming':{'r':54,'g':116,'b':125},
    'minion yellow':{'r':245,'g':224,'b':80},
    'mint':{'r':62,'g':180,'b':137},
    'mint cream':{'r':245,'g':255,'b':250},
    'mint green':{'r':152,'g':255,'b':152},
    'misty moss':{'r':187,'g':180,'b':119},
    'misty rose':{'r':255,'g':228,'b':225},
    'mode beige':{'r':150,'g':113,'b':23},
    'morning blue':{'r':141,'g':163,'b':153},
    'moss green':{'r':138,'g':154,'b':91},
    'mountain meadow':{'r':48,'g':186,'b':143},
    'mountbatten pink':{'r':153,'g':122,'b':141},
    'msu green':{'r':24,'g':69,'b':59},
    'mulberry':{'r':197,'g':75,'b':140},
    'mustard':{'r':255,'g':219,'b':88},
    'myrtle green':{'r':49,'g':120,'b':115},
    'mystic':{'r':214,'g':82,'b':130},
    'mystic maroon':{'r':173,'g':67,'b':121},
    'nadeshiko pink':{'r':246,'g':173,'b':198},
    'naples yellow':{'r':250,'g':218,'b':94},
    'navajo white':{'r':255,'g':222,'b':173},
    'navy blue':{'r':0,'g':0,'b':128},
    'neon blue':{'r':70,'g':102,'b':255},
    'neon carrot':{'r':255,'g':163,'b':67},
    'neon green':{'r':57,'g':255,'b':20},
    'neon fuchsia':{'r':254,'g':65,'b':100},
    'new york pink':{'r':215,'g':131,'b':127},
    'nickel':{'r':114,'g':116,'b':114},
    'non photo blue':{'r':164,'g':221,'b':237},
    'nyanza':{'r':233,'g':255,'b':219},
    'ocean blue':{'r':79,'g':66,'b':181},
    'ocean green':{'r':72,'g':191,'b':145},
    'ochre':{'r':204,'g':119,'b':34},
    'old burgundy':{'r':67,'g':48,'b':46},
    'old gold':{'r':207,'g':181,'b':59},
    'old lace':{'r':253,'g':245,'b':230},
    'old lavender':{'r':121,'g':104,'b':120},
    'old mauve':{'r':103,'g':49,'b':71},
    'old rose':{'r':192,'g':128,'b':129},
    'old silver':{'r':132,'g':132,'b':130},
    'olive':{'r':128,'g':128,'b':0},
    'olive drab':{'r':107,'g':142,'b':35},
    'olive drab #7':{'r':60,'g':52,'b':31},
    'olive green':{'r':181,'g':179,'b':92},
    'olivine':{'r':154,'g':185,'b':115},
    'onyx':{'r':53,'g':56,'b':57},
    'opal':{'r':168,'g':195,'b':188},
    'opera mauve':{'r':183,'g':132,'b':167},
    'orange':{'r':255,'g':127,'b':0},
    'orange peel':{'r':255,'g':159,'b':0},
    'orange red':{'r':255,'g':104,'b':31},
    'orange soda':{'r':250,'g':91,'b':61},
    'orange yellow':{'r':245,'g':189,'b':31},
    'orchid':{'r':218,'g':112,'b':214},
    'orchid pink':{'r':242,'g':189,'b':205},
    'orchid':{'r':226,'g':156,'b':210},
    'outer space':{'r':45,'g':56,'b':58},
    'outrageous orange':{'r':255,'g':110,'b':74},
    'oxblood':{'r':74,'g':0,'b':0},
    'oxford blue':{'r':0,'g':33,'b':71},
    'ou crimson red':{'r':132,'g':22,'b':23},
    'pacific blue':{'r':28,'g':169,'b':201},
    'pakistan green':{'r':0,'g':102,'b':0},
    'palatinate purple':{'r':104,'g':40,'b':96},
    'pale aqua':{'r':188,'g':212,'b':230},
    'pale cerulean':{'r':155,'g':196,'b':226},
    'pale dogwood':{'r':237,'g':122,'b':155},
    'pale pink':{'r':250,'g':218,'b':221},
    'pale purple':{'r':250,'g':230,'b':250},
    'pale silver':{'r':201,'g':192,'b':187},
    'pale spring bud':{'r':236,'g':235,'b':189},
    'pansy purple':{'r':120,'g':24,'b':74},
    'paolo veronese green':{'r':0,'g':155,'b':125},
    'papaya whip':{'r':255,'g':239,'b':213},
    'paradise pink':{'r':230,'g':62,'b':98},
    'parchment':{'r':241,'g':233,'b':210},
    'paris green':{'r':80,'g':200,'b':120},
    'pastel pink':{'r':222,'g':165,'b':164},
    'patriarch':{'r':128,'g':0,'b':128},
    'paynes grey':{'r':83,'g':104,'b':120},
    'peach':{'r':255,'g':229,'b':180},
    'peach puff':{'r':255,'g':218,'b':185},
    'pear':{'r':209,'g':226,'b':49},
    'pearly purple':{'r':183,'g':104,'b':162},
    'periwinkle':{'r':204,'g':204,'b':255},
    'permanent geranium lake':{'r':225,'g':44,'b':44},
    'persian blue':{'r':28,'g':57,'b':187},
    'persian green':{'r':0,'g':166,'b':147},
    'persian indigo':{'r':50,'g':18,'b':122},
    'persian orange':{'r':217,'g':144,'b':88},
    'persian pink':{'r':247,'g':127,'b':190},
    'persian plum':{'r':112,'g':28,'b':28},
    'persian red':{'r':204,'g':51,'b':51},
    'persian rose':{'r':254,'g':40,'b':162},
    'persimmon':{'r':236,'g':88,'b':0},
    'pewter blue':{'r':139,'g':168,'b':183},
    'phlox':{'r':223,'g':0,'b':255},
    'phthalo blue':{'r':0,'g':15,'b':137},
    'phthalo green':{'r':18,'g':53,'b':36},
    'picotee blue':{'r':46,'g':39,'b':135},
    'pictorial carmine':{'r':195,'g':11,'b':78},
    'piggy pink':{'r':253,'g':221,'b':230},
    'pine green':{'r':1,'g':121,'b':111},
    'pine tree':{'r':42,'g':47,'b':35},
    'pink':{'r':255,'g':192,'b':203},
    'pink flamingo':{'r':252,'g':116,'b':253},
    'pink lace':{'r':255,'g':221,'b':244},
    'pink lavender':{'r':216,'g':178,'b':209},
    'pink sherbet':{'r':247,'g':143,'b':167},
    'pistachio':{'r':147,'g':197,'b':114},
    'platinum':{'r':229,'g':228,'b':226},
    'plum':{'r':142,'g':69,'b':133},
    'plump purple':{'r':89,'g':70,'b':178},
    'polished pine':{'r':93,'g':164,'b':147},
    'pomp and power':{'r':134,'g':96,'b':142},
    'popstar':{'r':190,'g':79,'b':98},
    'portland orange':{'r':255,'g':90,'b':54},
    'powder blue':{'r':176,'g':224,'b':230},
    'princeton orange':{'r':245,'g':128,'b':37},
    'process yellow':{'r':255,'g':239,'b':0},
    'prune':{'r':112,'g':28,'b':28},
    'prussian blue':{'r':0,'g':49,'b':83},
    'psychedelic purple':{'r':223,'g':0,'b':255},
    'puce':{'r':204,'g':136,'b':153},
    'pullman brown':{'r':100,'g':65,'b':23},
    'pumpkin':{'r':255,'g':117,'b':24},
    'purple':{'r':106,'g':13,'b':173},
    'purple mountain majesty':{'r':150,'g':120,'b':182},
    'purple navy':{'r':78,'g':81,'b':128},
    'purple pizzazz':{'r':254,'g':78,'b':218},
    'purple plum':{'r':156,'g':81,'b':182},
    'purpureus':{'r':154,'g':78,'b':174},
    'queen blue':{'r':67,'g':107,'b':149},
    'queen pink':{'r':232,'g':204,'b':215},
    'quick silver':{'r':166,'g':166,'b':166},
    'quinacridone magenta':{'r':142,'g':58,'b':89},
    'radical red':{'r':255,'g':53,'b':94},
    'raisin black':{'r':36,'g':33,'b':36},
    'rajah':{'r':251,'g':171,'b':96},
    'raspberry':{'r':227,'g':11,'b':93},
    'raspberry glace':{'r':145,'g':95,'b':109},
    'raspberry rose':{'r':179,'g':68,'b':108},
    'raw sienna':{'r':214,'g':138,'b':89},
    'raw umber':{'r':130,'g':102,'b':68},
    'razzle dazzle rose':{'r':255,'g':51,'b':204},
    'razzmatazz':{'r':227,'g':37,'b':107},
    'razzmic berry':{'r':141,'g':78,'b':133},
    'rebecca purple':{'r':102,'g':51,'b':153},
    'red':{'r':255,'g':0,'b':0},
    'red orange':{'r':255,'g':83,'b':73},
    'red purple':{'r':228,'g':0,'b':120},
    'red salsa':{'r':253,'g':58,'b':74},
    'red violet':{'r':199,'g':21,'b':133},
    'redwood':{'r':164,'g':90,'b':82},
    'resolution blue':{'r':0,'g':35,'b':135},
    'rhythm':{'r':119,'g':118,'b':150},
    'rich black':{'r':0,'g':64,'b':64},
    'rifle green':{'r':68,'g':76,'b':56},
    'robin egg blue':{'r':0,'g':204,'b':204},
    'rocket metallic':{'r':138,'g':127,'b':128},
    'rojo spanish red':{'r':169,'g':17,'b':1},
    'roman silver':{'r':131,'g':137,'b':150},
    'rose':{'r':255,'g':0,'b':127},
    'rose bonbon':{'r':249,'g':66,'b':158},
    'rose dust':{'r':158,'g':94,'b':111},
    'rose ebony':{'r':103,'g':72,'b':70},
    'rose madder':{'r':227,'g':38,'b':54},
    'rose pink':{'r':255,'g':102,'b':204},
    'rose pompadour':{'r':237,'g':122,'b':155},
    'rose quartz':{'r':170,'g':152,'b':169},
    'rose red':{'r':194,'g':30,'b':86},
    'rose taupe':{'r':144,'g':93,'b':93},
    'rose vale':{'r':171,'g':78,'b':82},
    'rosewood':{'r':101,'g':0,'b':11},
    'rosso corsa':{'r':212,'g':0,'b':0},
    'rosy brown':{'r':188,'g':143,'b':143},
    'royal blue':{'r':0,'g':35,'b':102},
    'royal purple':{'r':120,'g':81,'b':169},
    'royal yellow':{'r':250,'g':218,'b':94},
    'ruber':{'r':206,'g':70,'b':118},
    'rubine red':{'r':209,'g':0,'b':86},
    'ruby':{'r':224,'g':17,'b':95},
    'ruby red':{'r':155,'g':17,'b':30},
    'rufous':{'r':168,'g':28,'b':7},
    'russet':{'r':128,'g':70,'b':27},
    'russian green':{'r':103,'g':146,'b':103},
    'russian violet':{'r':50,'g':23,'b':77},
    'rust':{'r':183,'g':65,'b':14},
    'rusty red':{'r':218,'g':44,'b':67},
    'sacramento state green':{'r':4,'g':57,'b':39},
    'saddle brown':{'r':139,'g':69,'b':19},
    'safety orange':{'r':255,'g':120,'b':0},
    'safety yellow':{'r':238,'g':210,'b':2},
    'saffron':{'r':244,'g':196,'b':48},
    'sage':{'r':188,'g':184,'b':138},
    'saint patricks blue':{'r':35,'g':41,'b':122},
    'salmon':{'r':250,'g':128,'b':114},
    'salmon pink':{'r':255,'g':145,'b':164},
    'sand':{'r':194,'g':178,'b':128},
    'sand dune':{'r':150,'g':113,'b':23},
    'sandy brown':{'r':244,'g':164,'b':96},
    'sap green':{'r':80,'g':125,'b':42},
    'sapphire':{'r':15,'g':82,'b':186},
    'sapphire blue':{'r':0,'g':103,'b':165},
    'sapphire':{'r':0,'g':103,'b':165},
    'satin sheen gold':{'r':203,'g':161,'b':53},
    'scarlet':{'r':255,'g':36,'b':0},
    'schauss pink':{'r':255,'g':145,'b':175},
    'school bus yellow':{'r':255,'g':216,'b':0},
    'screaming green':{'r':102,'g':255,'b':102},
    'sea green':{'r':46,'g':139,'b':87},
    'seal brown':{'r':89,'g':38,'b':11},
    'seashell':{'r':255,'g':245,'b':238},
    'selective yellow':{'r':255,'g':186,'b':0},
    'sepia':{'r':112,'g':66,'b':20},
    'shadow':{'r':138,'g':121,'b':93},
    'shadow blue':{'r':119,'g':139,'b':165},
    'shamrock green':{'r':0,'g':158,'b':96},
    'sheen green':{'r':143,'g':212,'b':0},
    'shimmering blush':{'r':217,'g':134,'b':149},
    'shiny shamrock':{'r':95,'g':167,'b':120},
    'shocking pink':{'r':252,'g':15,'b':192},
    'sienna':{'r':136,'g':45,'b':23},
    'silver':{'r':192,'g':192,'b':192},
    'silver chalice':{'r':172,'g':172,'b':172},
    'silver pink':{'r':196,'g':174,'b':173},
    'silver sand':{'r':191,'g':193,'b':194},
    'sinopia':{'r':203,'g':65,'b':11},
    'sizzling red':{'r':255,'g':56,'b':85},
    'sizzling sunrise':{'r':255,'g':219,'b':0},
    'skobeloff':{'r':0,'g':116,'b':116},
    'sky blue':{'r':135,'g':206,'b':235},
    'sky magenta':{'r':207,'g':113,'b':175},
    'slate blue':{'r':106,'g':90,'b':205},
    'slate gray':{'r':112,'g':128,'b':144},
    'slimy green':{'r':41,'g':150,'b':23},
    'smitten':{'r':200,'g':65,'b':134},
    'smoky black':{'r':16,'g':12,'b':8},
    'snow':{'r':255,'g':250,'b':250},
    'solid pink':{'r':137,'g':56,'b':67},
    'sonic silver':{'r':117,'g':117,'b':117},
    'space cadet':{'r':29,'g':41,'b':81},
    'spanish bistre':{'r':128,'g':117,'b':50},
    'spanish blue':{'r':0,'g':112,'b':184},
    'spanish carmine':{'r':209,'g':0,'b':71},
    'spanish gray':{'r':152,'g':152,'b':152},
    'spanish green':{'r':0,'g':145,'b':80},
    'spanish orange':{'r':232,'g':97,'b':0},
    'spanish pink':{'r':247,'g':191,'b':190},
    'spanish red':{'r':230,'g':0,'b':38},
    'spanish sky blue':{'r':0,'g':255,'b':255},
    'spanish violet':{'r':76,'g':40,'b':130},
    'spanish viridian':{'r':0,'g':127,'b':92},
    'spring bud':{'r':167,'g':252,'b':0},
    'spring frost':{'r':135,'g':255,'b':42},
    'spring green':{'r':0,'g':255,'b':127},
    'star command blue':{'r':0,'g':123,'b':184},
    'steel blue':{'r':70,'g':130,'b':180},
    'steel pink':{'r':204,'g':51,'b':204},
    'steel teal':{'r':95,'g':138,'b':139},
    'stil de grain yellow':{'r':250,'g':218,'b':94},
    'straw':{'r':228,'g':217,'b':111},
    'strawberry':{'r':250,'g':80,'b':83},
    'strawberry blonde':{'r':255,'g':147,'b':97},
    'sugar plum':{'r':145,'g':78,'b':117},
    'sunglow':{'r':255,'g':204,'b':51},
    'sunray':{'r':227,'g':171,'b':87},
    'sunset':{'r':250,'g':214,'b':165},
    'super pink':{'r':207,'g':107,'b':169},
    'sweet brown':{'r':168,'g':55,'b':49},
    'syracuse orange':{'r':212,'g':69,'b':0},
    'tan':{'r':210,'g':180,'b':140},
    'tangerine':{'r':242,'g':133,'b':0},
    'tango pink':{'r':228,'g':113,'b':122},
    'tart orange':{'r':251,'g':77,'b':70},
    'taupe':{'r':72,'g':60,'b':50},
    'taupe gray':{'r':139,'g':133,'b':137},
    'tea green':{'r':208,'g':240,'b':192},
    'tea rose':{'r':248,'g':131,'b':121},
    'teal':{'r':0,'g':128,'b':128},
    'teal blue':{'r':54,'g':117,'b':136},
    'telemagenta':{'r':207,'g':52,'b':118},
    'terra cotta':{'r':226,'g':114,'b':91},
    'thistle':{'r':216,'g':191,'b':216},
    'thulian pink':{'r':222,'g':111,'b':161},
    'tickle me pink':{'r':252,'g':137,'b':172},
    'tiffany blue':{'r':10,'g':186,'b':181},
    'timberwolf':{'r':219,'g':215,'b':210},
    'titanium yellow':{'r':238,'g':230,'b':0},
    'tomato':{'r':255,'g':99,'b':71},
    'tropical rainforest':{'r':0,'g':117,'b':94},
    'true blue':{'r':45,'g':104,'b':196},
    'trypan blue':{'r':28,'g':5,'b':179},
    'tufts blue':{'r':62,'g':142,'b':222},
    'tumbleweed':{'r':222,'g':170,'b':136},
    'turquoise':{'r':64,'g':224,'b':208},
    'turquoise blue':{'r':0,'g':255,'b':239},
    'turquoise green':{'r':160,'g':214,'b':180},
    'turtle green':{'r':138,'g':154,'b':91},
    'tuscan':{'r':250,'g':214,'b':165},
    'tuscan brown':{'r':111,'g':78,'b':55},
    'tuscan red':{'r':124,'g':72,'b':72},
    'tuscan tan':{'r':166,'g':123,'b':91},
    'tuscany':{'r':192,'g':153,'b':153},
    'twilight lavender':{'r':138,'g':73,'b':107},
    'tyrian purple':{'r':102,'g':2,'b':60},
    'ua blue':{'r':0,'g':51,'b':170},
    'ua red':{'r':217,'g':0,'b':76},
    'ultramarine':{'r':63,'g':0,'b':255},
    'ultramarine blue':{'r':65,'g':102,'b':245},
    'ultra pink':{'r':255,'g':111,'b':255},
    'ultra red':{'r':252,'g':108,'b':133},
    'umber':{'r':99,'g':81,'b':71},
    'unbleached silk':{'r':255,'g':221,'b':202},
    'united nations blue':{'r':91,'g':146,'b':229},
    'university of pennsylvania red':{'r':165,'g':0,'b':33},
    'unmellow yellow':{'r':255,'g':255,'b':102},
    'up forest green':{'r':1,'g':68,'b':33},
    'up maroon':{'r':123,'g':17,'b':19},
    'upsdell red':{'r':174,'g':32,'b':41},
    'uranian blue':{'r':175,'g':219,'b':245},
    'usafa blue':{'r':0,'g':79,'b':152},
    'van dyke brown':{'r':102,'g':66,'b':40},
    'vanilla':{'r':243,'g':229,'b':171},
    'vanilla ice':{'r':243,'g':143,'b':169},
    'vegas gold':{'r':197,'g':179,'b':88},
    'venetian red':{'r':200,'g':8,'b':21},
    'verdigris':{'r':67,'g':179,'b':174},
    'vermilion':{'r':227,'g':66,'b':52},
    'veronica':{'r':160,'g':32,'b':240},
    'violet':{'r':143,'g':0,'b':255},
    'violet blue':{'r':50,'g':74,'b':178},
    'violet red':{'r':247,'g':83,'b':148},
    'viridian':{'r':64,'g':130,'b':109},
    'viridian green':{'r':0,'g':150,'b':152},
    'vivid burgundy':{'r':159,'g':29,'b':53},
    'vivid sky blue':{'r':0,'g':204,'b':255},
    'vivid tangerine':{'r':255,'g':160,'b':137},
    'vivid violet':{'r':159,'g':0,'b':255},
    'volt':{'r':206,'g':255,'b':0},
    'warm black':{'r':0,'g':66,'b':66},
    'wheat':{'r':245,'g':222,'b':179},
    'white':{'r':255,'g':255,'b':255},
    'wild blue yonder':{'r':162,'g':173,'b':208},
    'wild orchid':{'r':212,'g':112,'b':162},
    'wild strawberry':{'r':255,'g':67,'b':164},
    'wild watermelon':{'r':252,'g':108,'b':133},
    'windsor tan':{'r':167,'g':85,'b':2},
    'wine':{'r':114,'g':47,'b':55},
    'wine dregs':{'r':103,'g':49,'b':71},
    'winter sky':{'r':255,'g':0,'b':124},
    'wintergreen dream':{'r':86,'g':136,'b':125},
    'wisteria':{'r':201,'g':160,'b':220},
    'wood brown':{'r':193,'g':154,'b':107},
    'xanadu':{'r':115,'g':134,'b':120},
    'xanthic':{'r':238,'g':237,'b':9},
    'xanthous':{'r':241,'g':180,'b':47},
    'yale blue':{'r':0,'g':53,'b':107},
    'yellow':{'r':255,'g':255,'b':0},
    'yellow green':{'r':154,'g':205,'b':50},
    'yellow orange':{'r':255,'g':174,'b':66},
    'yellow sunshine':{'r':255,'g':247,'b':0},
    'yinmn blue':{'r':46,'g':80,'b':144},
    'zaffre':{'r':0,'g':20,'b':168},
    'zomp':{'r':57,'g':167,'b':142}
}

def print_info(stick):
    print("Found device:")
    device=stick.get('device')
    print("    Manufacturer:  {0}".format(device.get_manufacturer()))
    print("    Description:   {0}".format(device.get_description()))
    print("    Variant:       {0}".format(device.get_variant_string()))
    print("    Serial:        {0}".format(device.get_serial()))
    print("    Mode:          {0}".format(device.get_mode()))
    if device.get_variant() == blinkstick.BlinkStick.BLINKSTICK_FLEX:
        print("    LED conf:      {0}".format(stick.get('maxLed')))
    print("    Info Block 1:  {0}".format(device.get_info_block1()))
    print("    Info Block 2:  {0}".format(device.get_info_block2()))
    
def max_leds(stick):
    count=-1
    try:
        count = stick.get_led_count()
    except:
        count = 32
    return count
    
def getRandomColor():
    r=int(random.random() *256)
    g=int(random.random() *256)
    b=int(random.random() *256)
    return r,g,b
    
def getStick(args):
    serial=args.get('deviceId')
    return devices[serial]

def getColorParams(args):
    r=int(args.get('r'))
    g=int(args.get('g'))
    b=int(args.get('b'))
    stick=getStick(args)
    return stick,r,g,b
    
def list():
    return devices.keys()
    
def setIndexedColor(stick,index,r,g,b):
    device=stick.get('device')
    index=int(index)
    device.set_color(red=applyBrightness(stick,r),green=applyBrightness(stick,g),blue=applyBrightness(stick,b),index=index)
    stick.get('colors')[index]={
                                'r':r, 
                                'g':g, 
                                'b':b
                                }
                                
def setStripColors(device,payload):
    device.set_led_data(0, payload)
    
def setStripColor(stick,r,g,b):
    device=stick.get('device')
    maxLED=stick.get('maxLed')
    setStripColors(device,[applyBrightness(stick,g), applyBrightness(stick,r), applyBrightness(stick,b)]*maxLED)
    stick['colors']=[{
                'r':r, 
                'g':g, 
                'b':b}]*maxLED
                
def setStripRandomLEDColors(stick):
    device=stick.get('device')
    maxLED=stick.get('maxLed')
    buffer=[]
    commandBuffer=[]
    for i in range(0,maxLED):
        r,g,b=getRandomColor()
        buffer.append({
                'r':r, 
                'g':g, 
                'b':b})
        commandBuffer.append(applyBrightness(stick,g))
        commandBuffer.append(applyBrightness(stick,r))
        commandBuffer.append(applyBrightness(stick,b))
    setStripColors(device,commandBuffer)
    
    stick['colors']=buffer
    
def setStripLEDColors(stick,payload):
    maxLED=stick.get('maxLed')
    if not (len(payload)==maxLED):
        print("ERROR not same size array:" + str(len(payload)) + ":" + str(maxLED))
        return
    device=stick.get('device')
    buffer=[]
    commandBuffer=[]
    for i in range(0,maxLED):
        r=payload[i]['r']
        g=payload[i]['g']
        b=payload[i]['b']
        buffer.append({
                'r':r, 
                'g':g, 
                'b':b})
        commandBuffer.append(applyBrightness(stick,g))
        commandBuffer.append(applyBrightness(stick,r))
        commandBuffer.append(applyBrightness(stick,b))
    setStripColors(device,commandBuffer)
    
    stick['colors']=buffer
    
def applyBrightness(stick,rgb):
    brightness=stick.get('brightness')
    return int(rgb*brightness)
    
def setBrightness(stick,brightness):
    device=stick.get('device')
    commandBuffer=[]
    stick['brightness']=brightness
    for color in stick.get('colors'):
        commandBuffer.append(applyBrightness(stick,color.get('g')))
        commandBuffer.append(applyBrightness(stick,color.get('r')))
        commandBuffer.append(applyBrightness(stick,color.get('b')))
    
    setStripColors(device,commandBuffer)

def playanimation(stick,delay,stripCommands):
    for i in range(0,len(stripCommands)):
        content=stripCommands[i]
        setStripLEDColors(stick,content)
        if(stick['animationThread']=="Stopping"):
            raise StopIteration
        time.sleep(delay / 1000.0)
    
def startAnimation(stick,delay,count,persistent,stripCommands):
    try:
        if count > 0:
            for loopi in range(0,count):
                playanimation(stick,delay,stripCommands)
        else:
            while(True):
                playanimation(stick,delay,stripCommands)
    except StopIteration:
        print "Caught"
    if not (persistent == True):
        setStripColor(stick,0,0,0) # prevent staying in last state
    stick['animationThread']="Stopped"
    

def main():
    global devices
    devices={}
    detectedSources = blinkstick.find_all()
    for device in detectedSources:
        maxLED=max_leds(device)
        devices[device.get_serial()]={
            'maxLed':maxLED,
            'device':device,
            'colors':[{
                'r':0, 
                'g':0, 
                'b':0}]*maxLED,
            'brightness':1,
            'animationThread':"Stopped"
        }
        setStripColor(devices[device.get_serial()],0,0,0)
        print_info(devices[device.get_serial()])

    api = Flask(__name__)

    @api.route('/list', methods=['GET'])
    def get_devices():
      return Response(json.dumps(list()), mimetype="application/json")
      
    @api.route('/setColor', methods=['GET'])
    def set_one_color():
        try:
            stick,r,g,b=getColorParams(request.args)
            
            if("index" in request.args):
                setIndexedColor(stick,request.args.get('index'),r,g,b)
            else:
                setStripColor(stick,r,g,b)
            return Response(json.dumps({"success":True}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")
            
    @api.route('/setColors', methods=['POST'])
    def set_strip_colors():
        try:
            stick=getStick(request.args)
            content=request.json
            setStripLEDColors(stick,content)
            return Response(json.dumps({"success":True}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")
            
    @api.route('/setRandom', methods=['GET'])
    def set_random_same_color():
        try:
            stick=getStick(request.args)
            r,g,b=getRandomColor()
            if("index" in request.args):
                setIndexedColor(stick.get('device'),request.args.get('index'),r,g,b)
            else:
                setStripColor(stick,r,g,b)
            return Response(json.dumps({"success":True}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")

    @api.route('/getColor', methods=['GET'])
    def get_all_colors():
        try:
            stick=getStick(request.args)
            colors=stick.get('colors')
            if("index" in request.args):
                return Response(json.dumps({"success":True,"color":colors.get(request.args.get('index'))}), mimetype="application/json")
            else:
                return Response(json.dumps({"success":True,"colors":colors}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")

    @api.route('/getNamedColor', methods=['GET'])
    def get_named_color():
        try:
            nameProvided=request.args.get('name').lower()
            if nameProvided in named_colors:
                return Response(json.dumps(named_colors[nameProvided]), mimetype="application/json")
            else:
                return Response(json.dumps(named_colors['']), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")
            
    @api.route('/setAllRandom', methods=['GET'])
    def set_random_individual_color():
        try:
            stick=getStick(request.args)
            setStripRandomLEDColors(stick)
            return Response(json.dumps({"success":True}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")

    @api.route('/setBrightness', methods=['GET'])
    def set_brightness():
        try:
            stick=getStick(request.args)
            brightness=float(request.args.get('percent'))
            setBrightness(stick,brightness)
            return Response(json.dumps({"success":True}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")
            
    @api.route('/startAnimation', methods=['POST'])
    def start_animation():
        try:
            stick=getStick(request.args)
            animationContent=request.json
            delay=animationContent['delay']
            count=animationContent['count']
            persistent=animationContent['persistent']
            stripCommands=animationContent['commands']
            if not(stick.get('animationThread') == "Stopped"):
                return Response(json.dumps({"success":False,"error":"Animation is currently " + stick.get('animationThread') + ", cancel with /stopAnimation"}), mimetype="application/json")
            
            thread = Thread(target = startAnimation, args = (stick,delay,count,persistent,stripCommands, ))
            thread.start()
            stick['animationThread']="Running"
            
            return Response(json.dumps({"success":True}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")
            
    @api.route('/stopAnimation', methods=['GET'])
    def stop_animation():
        try:
            stick=getStick(request.args)
            if not(stick.get('animationThread') == "Stopped"):
                stick['animationThread']="Stopping"
            while not (stick.get('animationThread') == "Stopped"):
                status="waiting to stop"
            return Response(json.dumps({"success":True}), mimetype="application/json")
        except Exception as error:
            return Response(json.dumps({"success":False,"error":str(error)}), mimetype="application/json")
            
    @api.route('/web', methods=['GET'])
    def show_demo_page():
        return """
        <html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Testing platform</title>
<style>

html,body {
	background:#0d4d2b;
}

.whitebg{
	background:white;
}

.group {
	display:block;
	width:(100% - 10px);
	height:auto;
	min-height:40px;
	padding:5px;
}

input[type="color"] {
    -webkit-appearance: none;
    border: solid 0px #11ef88;
    width: 20px;
    height: 20px;
    padding: 0;
    margin: 0;
    display: block;
    float: left;
}

input[type="color"]::-webkit-color-swatch-wrapper {
	padding:0;
	margin:0;
	border: solid 0px transparent;
	border-radius: 40px;
}


</style>
<script>

waiting=false;
lastUrl=""
function pendingCheck(responseText)
{
	insaneFramerate(false);
	waiting=false;
	if(lastUrl!="")
	{
		httpGetAsync(lastUrl, pendingCheck)
		lastUrl="";
	}
}

function httpGetAsync(theUrl, callback)
{
	if(waiting==false)
	{
		waiting=true;
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.onreadystatechange = function() { 
			if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
				callback(xmlHttp.responseText);
		}
		xmlHttp.open("GET", theUrl, true); // true for asynchronous 
		xmlHttp.send(null);
	}
	else
	{
		lastUrl=theUrl;
	}
}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

function fireColorChange(id,hex)
{
	rgb=hexToRgb(hex)
	if(id=="all")
	{
		httpGetAsync("/setColor?deviceId=BS036121-3.1&r=" + rgb['r'] + "&g=" + rgb['g'] + "&b=" + rgb['b'],pendingCheck);
		/*inputs = document.getElementsByTagName('input');
		for (index = 0; index < inputs.length; ++index) {
			if(inputs[index].getAttribute('type')=='color')
			{
				inputs[index].value=hex;
			}
		}*/
		document.getElementById('all').style.opacity=1;
	}
	else
	{
		httpGetAsync("/setColor?deviceId=BS036121-3.1&r=" + rgb['r'] + "&g=" + rgb['g'] + "&b=" + rgb['b'] + "&index=" + id ,pendingCheck);
		document.getElementById('all').style.opacity=0.5;
	}
}

function componentToHex(c) {
	if(c > 255)
	{
		c=255;
	}
	if(c < 0)
	{
		c=-1;
	}
	  var hex = c.toString(16);
	  return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(point)
{
    r=componentToHex(point['r']);
	g=componentToHex(point['g']);
	b=componentToHex(point['b']);
	return "#" + r + g + b;
}

function httpGetAsyncSpecial(theUrl, callback)
{
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() { 
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
		{
			callback(xmlHttp.responseText);
		}
	}
	xmlHttp.open("GET", theUrl, true); // true for asynchronous 
	try
	{
		xmlHttp.send(null);
	}
	catch(e)
	{
		callback("");
	}
}

function colorCheck(responseText)
{
	var points = JSON.parse(responseText)["colors"];
    for (id = 0; id < points.length; id++) {
		document.getElementById(id).value=rgbToHex(points[id]);
	}
	
}

framerate=1000;
function insaneFramerate(really)
{
	if(really)
	{
		framerate=1;
	}
	else{
		framerate=1000;
	}
}

function colorCheckLoop()
{
	httpGetAsyncSpecial('/getColor?deviceId=BS036121-3.1', colorCheck)
	setTimeout(colorCheckLoop,framerate);
}

function allOn()
{
	httpGetAsyncSpecial("/setColor?deviceId=BS036121-3.1&r=255&g=255&b=255" ,pendingCheck);
}
function allOff()
{
	httpGetAsyncSpecial("/setColor?deviceId=BS036121-3.1&r=0&g=0&b=0" ,pendingCheck);
}
function allRandom()
{
	httpGetAsyncSpecial("/setRandom?deviceId=BS036121-3.1" ,pendingCheck);
}

function allMultiRandom()
{
	httpGetAsyncSpecial("/setAllRandom?deviceId=BS036121-3.1" ,pendingCheck);
}

function setBrightness(value)
{
	httpGetAsync("/setBrightness?deviceId=BS036121-3.1&percent=" + (value/100),pendingCheck);
}

</script>

</head>
<body onload="colorCheckLoop()">
<div class="group">
    <input type="color" id="all" name="all" value="#000000" oninput="fireColorChange(this.id,this.value);">
    <label for="all">All</label>
</div>
<div class="group">
	<input type="range" min="1" max="100" value="5" name="myPercent" oninput="setBrightness(this.value)">
	<label for="myPercent">Brightness</label>
</div>
<div class="group">
	<input type="color" id="0" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="1" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="2" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="3" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="4" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="5" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="6" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="7" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="8" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="9" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="10" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="11" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="12" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="13" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="14" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="15" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="16" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="17" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="18" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="19" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="20" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="21" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="22" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="23" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="24" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="25" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="26" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="27" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="28" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="29" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="30" value="#000000" oninput="fireColorChange(this.id,this.value);">
	<input type="color" id="31" value="#000000" oninput="fireColorChange(this.id,this.value);">
</div>
<div class="group whitebg">
	<button onclick="allOn()">All White</button><br/>
	<button onclick="allOff()">All Off/black</button><br/>
	<button onclick="allRandom()">All (one) Random</button><br/>
	<button onclick="allMultiRandom()">All (multiple) Random</button><br/>
</div>

</body>
</html>
"""
            
    api.run(host='0.0.0.0',port=80)
      
        
    

    



if __name__ == '__main__':
    main()