from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from articles.models import Article, Category, Tag, Source
from games.models import Game


CATEGORIES = [
    {'name': 'Esports', 'slug': 'esports'},
    {'name': 'Game Reviews', 'slug': 'game-reviews'},
    {'name': 'Hardware', 'slug': 'hardware'},
    {'name': 'PC Gaming', 'slug': 'pc-gaming'},
    {'name': 'Console Gaming', 'slug': 'console-gaming'},
    {'name': 'Mobile Gaming', 'slug': 'mobile-gaming'},
    {'name': 'Industry News', 'slug': 'industry-news'},
    {'name': 'Indie Games', 'slug': 'indie-games'},
]

TAGS = [
    {'name': 'League of Legends', 'slug': 'league-of-legends', 'type': 'game'},
    {'name': 'Valorant', 'slug': 'valorant', 'type': 'game'},
    {'name': 'Elden Ring', 'slug': 'elden-ring', 'type': 'game'},
    {'name': 'GTA VI', 'slug': 'gta-vi', 'type': 'game'},
    {'name': 'PC', 'slug': 'pc', 'type': 'platform'},
    {'name': 'PlayStation 5', 'slug': 'playstation-5', 'type': 'platform'},
    {'name': 'Xbox', 'slug': 'xbox', 'type': 'platform'},
    {'name': 'FPS', 'slug': 'fps', 'type': 'genre'},
    {'name': 'RPG', 'slug': 'rpg', 'type': 'genre'},
    {'name': 'Battle Royale', 'slug': 'battle-royale', 'type': 'genre'},
    {'name': 'Breaking News', 'slug': 'breaking-news', 'type': 'general'},
    {'name': 'Tournament', 'slug': 'tournament', 'type': 'general'},
]

GAMES = [
    {
        'title': 'Valorant',
        'description': 'A 5v5 character-based tactical shooter by Riot Games set in the near future.',
        'short_description': 'Riot Games\' free-to-play tactical FPS.',
        'genre': 'Tactical Shooter',
        'platforms': ['PC'],
        'developer': 'Riot Games',
        'publisher': 'Riot Games',
        'release_display': 'Released',
        'game_type': 'popular',
        'status': 'released',
        'popularity_score': 95,
        'player_count': '14M+',
        'metacritic': 80,
        'rating': 4.5,
        'rank': 1,
        'trend': 'up',
    },
    {
        'title': 'Elden Ring',
        'description': 'An action RPG developed by FromSoftware and published by Bandai Namco. Set in the Lands Between.',
        'short_description': 'FromSoftware\'s open-world soulslike masterpiece.',
        'genre': 'Action RPG',
        'platforms': ['PC', 'PS5', 'Xbox Series X'],
        'developer': 'FromSoftware',
        'publisher': 'Bandai Namco',
        'release_display': 'Released',
        'game_type': 'popular',
        'status': 'released',
        'popularity_score': 97,
        'player_count': '20M+',
        'metacritic': 96,
        'rating': 4.8,
        'rank': 2,
        'trend': 'stable',
    },
    {
        'title': 'GTA VI',
        'description': 'The next chapter in Rockstar\'s Grand Theft Auto series, set in Vice City and surrounding areas.',
        'short_description': 'Rockstar\'s most anticipated open-world game ever.',
        'genre': 'Open World Action',
        'platforms': ['PS5', 'Xbox Series X'],
        'developer': 'Rockstar Games',
        'publisher': 'Rockstar Games',
        'release_display': '2025',
        'game_type': 'anticipated',
        'status': 'coming_soon',
        'hype_score': 99,
        'rank': 1,
        'trend': 'up',
    },
    {
        'title': 'League of Legends',
        'description': 'A fast-paced, competitive online game where two teams of five battle to destroy the opposing Nexus.',
        'short_description': 'The world\'s most popular MOBA.',
        'genre': 'MOBA',
        'platforms': ['PC'],
        'developer': 'Riot Games',
        'publisher': 'Riot Games',
        'release_display': 'Released',
        'game_type': 'popular',
        'status': 'released',
        'popularity_score': 98,
        'player_count': '150M+',
        'metacritic': 78,
        'rating': 4.3,
        'rank': 3,
        'trend': 'stable',
    },
    {
        'title': 'Hollow Knight: Silksong',
        'description': 'The eagerly awaited sequel to Hollow Knight, following Hornet on her journey through a vast new kingdom.',
        'short_description': 'Team Cherry\'s long-awaited metroidvania sequel.',
        'genre': 'Metroidvania',
        'platforms': ['PC', 'Nintendo Switch', 'PS5', 'Xbox Series X'],
        'developer': 'Team Cherry',
        'publisher': 'Team Cherry',
        'release_display': 'TBA',
        'game_type': 'anticipated',
        'status': 'tba',
        'hype_score': 94,
        'rank': 2,
        'trend': 'up',
    },
]

ARTICLES = [
    {
        'title': 'T1 Clinches Worlds 2025 Championship Title in Dominant Fashion',
        'category': 'esports',
        'tags': ['league-of-legends', 'tournament'],
        'is_featured': True,
        'is_breaking': True,
        'content': """T1 have cemented their legacy as the greatest esports organization in history after claiming the League of Legends World Championship 2025 title in a breathtaking five-game series against Gen.G.

Lee "Faker" Sang-hyeok, widely regarded as the GOAT of competitive League of Legends, delivered a masterclass performance across all five games, earning unanimous MVP honors from a panel of analysts worldwide.

The series went the full five games, with T1 dropping games two and three before mounting a spectacular comeback. Faker's Orianna in game five produced one of the most celebrated Shockwave combinations in Worlds history, wiping out all five opponents during a crucial Baron contest.

"This championship means everything to me and to the fans," Faker said during the post-match interview. "We never stopped believing, even when we were down 1-2. This team fights until the very last second."

T1 becomes the first organization to win five World Championships, with their previous titles coming in 2013, 2015, 2016, and 2023. The victory secures a record $2.5 million prize pool split.

Gen.G put up a valiant effort and their bot lane duo of Ruler and Lehends were exceptional throughout the tournament, but T1's teamfighting and Faker's individual brilliance ultimately proved too much to overcome.

The trophy ceremony drew an in-person crowd of 60,000 fans at the Seoul World Cup Stadium, with tens of millions watching worldwide via live streams.""",
        'meta_title': 'T1 Wins Worlds 2025 — Faker Claims Historic 5th Championship',
        'meta_description': 'T1 defeat Gen.G 3-2 to win the 2025 LoL World Championship. Faker earns MVP with a legendary Orianna performance.',
        'status': 'publie',
    },
    {
        'title': 'Elden Ring: Shadow of the Erdtree DLC Review — A Masterpiece Within a Masterpiece',
        'category': 'game-reviews',
        'tags': ['elden-ring', 'rpg', 'pc', 'playstation-5'],
        'is_featured': True,
        'is_breaking': False,
        'content': """FromSoftware's Shadow of the Erdtree is not just a DLC — it is a full-scale expansion that rivals the base game in both scope and ambition. After dozens of hours exploring the Land of Shadow, one thing is crystal clear: this is the best piece of downloadable content ever made for an action RPG.

**A New World Worth Getting Lost In**

The Land of Shadow is hauntingly beautiful. From the golden fields of the Gravesite Plain to the oppressive gloom of the Realm of Shadow's deeper regions, every area feels hand-crafted with the obsessive attention to detail FromSoftware is known for. The verticality rivals some of the best areas in the base game, with multiple layers of secrets tucked into every corner.

**Boss Design at Its Peak**

Messmer the Impaler stands alongside Malenia as one of FromSoftware's all-time greatest boss encounters. His moveset is aggressive, relentless, and visually spectacular. The Scadutree Avatar and Romina, Saint of the Bud also leave lasting impressions.

**New Weapons and Build Variety**

Throwing knives, backhand blades, and the new martial arts fist weapons open up entirely new build archetypes. The Scadutree Fragments system — a parallel levelling mechanic exclusive to the DLC — keeps progression feeling meaningful throughout.

**Verdict: 10/10**

Shadow of the Erdtree is a landmark achievement in game design. Essential for any fan of the medium.""",
        'meta_title': 'Elden Ring Shadow of the Erdtree DLC Review — 10/10',
        'meta_description': 'Our full review of Elden Ring: Shadow of the Erdtree. A masterpiece DLC with incredible bosses, a stunning new world, and brilliant build variety.',
        'status': 'publie',
    },
    {
        'title': 'NVIDIA GeForce RTX 5090 Review: The New King of Gaming GPUs',
        'category': 'hardware',
        'tags': ['pc'],
        'is_featured': False,
        'is_breaking': False,
        'content': """NVIDIA's GeForce RTX 5090 is the most powerful consumer graphics card ever built, and after two weeks of testing across dozens of games and workloads, it earns that title handily — though its $1,999 price tag means most gamers will be watching from the sidelines.

**Performance**

At 4K resolution, the RTX 5090 delivers frame rates that were previously unthinkable. In Cyberpunk 2077 with path tracing and DLSS 4 enabled, we averaged 142 FPS at 4K — a 58% improvement over the RTX 4090. In more traditional rasterization workloads, gains average around 35-45%.

The new Blackwell architecture introduces fifth-generation Tensor Cores and improved RT Cores, making DLSS 4 with Multi Frame Generation the star of the show. With MFG active, frame rates can more than double.

**Thermals and Power**

The RTX 5090 draws up to 575W under full load, requiring a 1000W+ PSU for a comfortable headroom margin. Temperatures topped out at 83°C in our test bench with adequate case airflow — manageable but demanding.

**Memory**

32GB of GDDR7 memory running at 28 Gbps ensures the RTX 5090 will handle every resolution and texture setting available today, and then some. This future-proofing is a genuine selling point.

**Verdict**

The RTX 5090 is the undisputed performance champion, but at $1,999 it remains a product for enthusiasts with very deep pockets. If you need the best and price is no object, there is nothing better.""",
        'meta_title': 'NVIDIA RTX 5090 Review — The Fastest GPU Ever Made',
        'meta_description': 'Full benchmarks and review of the NVIDIA GeForce RTX 5090. Is this $1,999 GPU worth it? We find out.',
        'status': 'publie',
    },
    {
        'title': 'Valorant Champions Tour 2025: Everything You Need to Know',
        'category': 'esports',
        'tags': ['valorant', 'fps', 'tournament'],
        'is_featured': False,
        'is_breaking': False,
        'content': """Riot Games has unveiled the full details for the Valorant Champions Tour (VCT) 2025 season, featuring an expanded global league structure, increased prize pools, and a revamped Challengers pathway designed to elevate the next generation of professional talent.

**League Structure**

VCT 2025 will maintain the three international leagues — Americas, EMEA, and Pacific — with each featuring 10 partnered organizations competing in a split format. The top teams from each league will qualify for two international events: Masters Bangkok in April and Champions Istanbul in August.

**Prize Pool Increases**

The total prize pool across VCT 2025 has grown to $12 million, with Champions offering a $4 million prize pool — the largest in Valorant esports history. Riot also confirmed an increase in team stipends and player minimum salaries across all partnered leagues.

**Challengers Expansion**

The Challengers pathway, which feeds talent into the partnered leagues through the Ascension tournaments, will expand to 16 regions in 2025. This represents the most accessible season in VCT history for aspiring professionals outside the main leagues.

**Key Dates**

- VCT Americas Kickoff: January 15
- VCT EMEA Kickoff: January 17
- Masters Bangkok: April 18 – May 4
- VCT Americas Stage 1: February – March
- Champions Istanbul: August 8 – September 7

Team Liquid and Sentinels are among the early betting favorites in EMEA and Americas respectively, while Paper Rex look poised to dominate the Pacific league once again.""",
        'meta_title': 'VCT 2025 Season Guide — Dates, Prizes, and Format Explained',
        'meta_description': 'Everything you need to know about the Valorant Champions Tour 2025 season, including schedules, prize pools, and team rosters.',
        'status': 'publie',
    },
    {
        'title': 'GTA VI Release Window Confirmed: What We Know So Far',
        'category': 'industry-news',
        'tags': ['gta-vi', 'playstation-5', 'xbox'],
        'is_featured': True,
        'is_breaking': True,
        'content': """Rockstar Games has officially confirmed that Grand Theft Auto VI will launch in Fall 2025 for PlayStation 5 and Xbox Series X|S, putting an end to months of speculation about potential delays following the game's announcement trailer in December 2023.

**What the Trailer Showed Us**

The first trailer for GTA VI introduced Lucia, the franchise's first playable female protagonist, alongside her partner Jason. Set in a fictionalized Miami — Vice City and the surrounding Leonida state — the game's world appears to be the most visually stunning Rockstar has ever built.

The trailer showcased a living, breathing open world with unprecedented detail: realistic water simulations, dynamic weather systems, realistic crowd behavior, and an economy that appears to respond to player actions.

**No PC at Launch**

Rockstar confirmed the game will launch exclusively on PS5 and Xbox Series X|S, with a PC version expected 12-18 months later — consistent with Rockstar's historical release pattern with GTA V and Red Dead Redemption 2.

**Multiplayer Plans**

While story details remain under wraps, multiple industry insiders report that GTA Online 2 will launch alongside the single-player campaign, supporting up to 32 players per session. Cross-play between PS5 and Xbox has been hinted at but not confirmed.

**Pricing**

The game is expected to launch at $70 standard edition and $100 for the premium edition, which reportedly includes early access and the first batch of story DLC.

This will be the most anticipated game launch in history. Rockstar's last entry, GTA V, has sold over 195 million copies and remains one of the best-selling entertainment products of all time.""",
        'meta_title': 'GTA VI Release Date Confirmed — Fall 2025 for PS5 and Xbox',
        'meta_description': 'Rockstar confirms GTA VI for Fall 2025. Here\'s everything we know about the story, world, multiplayer, and pricing.',
        'status': 'publie',
    },
    {
        'title': 'Best Budget Gaming PCs Under $800 in 2025',
        'category': 'pc-gaming',
        'tags': ['pc'],
        'is_featured': False,
        'is_breaking': False,
        'content': """Building or buying a capable gaming PC doesn't have to cost a fortune. With the right components, you can put together a machine that handles 1080p gaming at high settings — and even dips into 1440p — for under $800. Here are our top picks and build recommendations.

**Best Pre-Built: Skytech Blaze 4.0**

The Skytech Blaze 4.0 packages a Ryzen 5 7600, 16GB DDR5 RAM, and an RX 7600 XT into a clean mid-tower case for $749. In our benchmarks it averaged 112 FPS in Fortnite, 87 FPS in Cyberpunk 2077, and 144+ FPS in CS2, all at 1080p high settings.

**Best DIY Build: ~$780**

| Component | Choice | Price |
|---|---|---|
| CPU | AMD Ryzen 5 7600 | $179 |
| GPU | RX 7600 XT 16GB | $279 |
| Motherboard | MSI PRO B650-P WiFi | $119 |
| RAM | 16GB DDR5-5600 | $54 |
| SSD | Samsung 870 EVO 1TB | $79 |
| PSU | EVGA 650 GQ | $69 |

Total: ~$779

This DIY build outperforms most pre-builts at its price point and gives you the satisfaction of knowing every component inside your machine.

**What to Expect**

At this price tier you should expect excellent 1080p performance in all modern titles, decent 1440p in less demanding games, and strong performance in esports titles at very high frame rates. Ray tracing will be limited, but everything else runs beautifully.""",
        'meta_title': 'Best Gaming PCs Under $800 in 2025 — Pre-Built and DIY',
        'meta_description': 'The best budget gaming PC builds and pre-built options for under $800 in 2025. Great 1080p performance without breaking the bank.',
        'status': 'publie',
    },
    {
        'title': 'PlayStation 5 Pro Full Review: Is the Upgrade Worth It?',
        'category': 'console-gaming',
        'tags': ['playstation-5', 'rpg'],
        'is_featured': False,
        'is_breaking': False,
        'content': """Sony's PlayStation 5 Pro arrives as the mid-generation refresh the company has been hinting at for years, packing a significantly more powerful GPU, a new PlayStation Spectral Super Resolution (PSSR) upscaling system, and support for 4K 60fps in games that previously ran at 30fps or only offered 60fps at reduced resolution.

**Hardware Improvements**

The PS5 Pro's GPU offers roughly 45% more raw compute performance than the standard PS5. Combined with PSSR — Sony's AI-powered upscaling technology trained on large datasets — the results are genuinely impressive. Games like Spider-Man 2 and Demon's Souls look noticeably sharper than their PS5 counterparts, with smoother frame pacing across the board.

**The Disc Drive Situation**

The PS5 Pro launches without a disc drive at $699 — a $100 premium over the standard disc edition PS5 at launch. An optional disc drive add-on costs an additional $79.99, bringing the total to nearly $780 for a complete physical-media setup. This is a significant ask.

**Game Performance**

We tested the PS5 Pro across 20 games. Highlights:
- Horizon Forbidden West: now 60fps in quality mode (was 30fps)
- Ratchet & Clank Rift Apart: 4K 60fps with ray tracing (was a choice between RT at 30fps or performance at 60fps)
- The Last of Us Part I: consistent 60fps across all scenes, no drops

**Verdict: 8/10**

The PS5 Pro is a genuine upgrade for 4K TV owners who want the best possible console gaming experience. The lack of a disc drive and $699 price make it a hard recommendation for casual players, but dedicated fans of Sony's first-party lineup will find the investment worthwhile.""",
        'meta_title': 'PS5 Pro Review — Worth the $699 Upgrade?',
        'meta_description': 'Our full PS5 Pro review. Better GPU, PSSR upscaling, and 4K 60fps upgrades — but is it worth $699 with no disc drive?',
        'status': 'publie',
    },
    {
        'title': 'Mobile Gaming Revenue Hits $100 Billion: The Games Driving Growth',
        'category': 'mobile-gaming',
        'tags': ['breaking-news'],
        'is_featured': False,
        'is_breaking': False,
        'content': """The global mobile gaming market has crossed the $100 billion annual revenue milestone for the first time, according to data released by Newzoo's 2025 Global Games Market Report. Mobile now accounts for 52% of total gaming industry revenue, outpacing PC and console combined.

**The Top Earners**

PUBG Mobile and Honor of Kings (known as Arena of Valor in the West) remain the two highest-grossing mobile games globally, each generating over $2 billion annually. Genshin Impact has crossed the $4 billion lifetime revenue mark since its 2020 launch, making it the most commercially successful mobile RPG ever made.

**What's Driving Growth**

Three key factors account for the market's sustained growth:
1. **Expanded internet access** in South and Southeast Asia, driven by affordable 5G devices
2. **Premium mobile experiences** — games like Diablo Immortal, Warcraft Rumble, and Pokémon UNITE offering near-console quality gameplay
3. **Live service monetization** — battle passes, limited-time events, and cosmetics replacing the pay-to-win models that drove users away in the early 2010s

**Regional Breakdown**

Asia-Pacific accounts for 55% of mobile gaming revenue, with China alone responsible for 23% of the global total. North America and Europe together contribute 33%, with the remaining 12% split across Latin America, the Middle East, and Africa.

**Looking Ahead**

Cloud gaming and AI-generated content are identified as the two technologies most likely to reshape mobile gaming over the next five years, according to Newzoo's analyst panel.""",
        'meta_title': 'Mobile Gaming Hits $100B Revenue — The Games Leading the Way',
        'meta_description': 'Global mobile gaming revenue crosses $100 billion for the first time. Which games are driving the growth and what comes next?',
        'status': 'publie',
    },
    {
        'title': 'Hollow Knight: Silksong Gets a Firm Release Date — Finally',
        'category': 'indie-games',
        'tags': ['breaking-news', 'pc', 'playstation-5', 'xbox'],
        'is_featured': True,
        'is_breaking': True,
        'content': """After years of anticipation and more memes about delays than any game in recent memory, Team Cherry has officially announced that Hollow Knight: Silksong will release on February 14, 2026 for PC, Nintendo Switch, PlayStation 5, and Xbox Series X|S.

The announcement came during a Nintendo Direct, where a new extended gameplay trailer showcased Hornet's fluid combat, the new needle weapon system, and a glimpse of the Citadel — a towering new area that appears to span multiple biomes within a single vertical structure.

**What We Saw in the Trailer**

The 7-minute gameplay showcase revealed:
- Over 40 new enemy types, including several spectacular mid-boss encounters
- Hornet's expanded moveset, featuring acrobatic aerial combos and the signature needle-and-thread silk abilities
- A day/night cycle that alters enemy behavior and reveals new paths
- A mysterious NPC faction called the Weavers who appear to have a central role in the story
- Silksong's version of charm-like abilities, called Threads, which can be combined for unique effects

**Day-One Game Pass and PS Plus**

Microsoft confirmed Silksong will be available on Game Pass from day one, while PlayStation confirmed it will launch as a PS Plus Extra title simultaneously.

**Collector's Edition**

Limited Run Games will produce a physical Collector's Edition containing the game, an art book, a silk map, an enamel pin set, and a Hornet statue. Pre-orders open next week.

The original Hollow Knight remains one of the highest-rated indie games of all time, with a 90 on Metacritic and over 5 million copies sold. Expectations for Silksong are stratospheric.""",
        'meta_title': 'Hollow Knight: Silksong Release Date — February 14, 2026',
        'meta_description': 'Team Cherry officially confirms Hollow Knight: Silksong launches February 14, 2026. Here\'s everything shown in the new gameplay trailer.',
        'status': 'publie',
    },
    {
        'title': 'Microsoft Acquires Ubisoft in $19 Billion Deal — What It Means for Gaming',
        'category': 'industry-news',
        'tags': ['breaking-news', 'xbox'],
        'is_featured': False,
        'is_breaking': True,
        'content': """In a seismic move that reshapes the games industry landscape, Microsoft has announced the acquisition of Ubisoft for $19 billion in an all-cash deal, subject to regulatory approval. If cleared, this would be the second-largest acquisition in gaming history, behind only Microsoft's $68.7 billion purchase of Activision Blizzard.

**What's in the Deal**

The acquisition brings Microsoft the full Ubisoft portfolio, which includes some of the most recognizable franchises in gaming: Assassin's Creed, Far Cry, Rainbow Six, The Division, Watch Dogs, Just Dance, and the Prince of Persia series. Ubisoft's studios in Montreal, Paris, Toronto, and Kyiv would all become part of Xbox Game Studios.

**Game Pass Implications**

Microsoft confirmed that all future Ubisoft titles — including the long-anticipated Assassin's Creed Shadows sequel and the next mainline Far Cry — will launch day-one on Xbox Game Pass. Existing Ubisoft back-catalog titles will gradually migrate to Game Pass over the next 18 months.

**Platform Parity Statement**

In a statement likely aimed at regulators, Xbox head Phil Spencer confirmed: "Ubisoft games will continue to be developed for and released on PlayStation. We are committed to supporting all platforms." This echoes similar commitments made during the Activision Blizzard acquisition process.

**Regulatory Hurdles**

Analysts expect the deal to face scrutiny from the European Commission and the UK's Competition and Markets Authority, both of which investigated the Activision Blizzard deal extensively before approving it. The process could take 12-18 months.

**What This Means for Players**

In the short term, little changes. In the long term, Xbox Game Pass subscribers gain access to one of the industry's largest open-world game franchises at no additional cost — a compelling value proposition that further distances Game Pass from its competitors.""",
        'meta_title': 'Microsoft Acquires Ubisoft for $19 Billion — Full Details',
        'meta_description': 'Microsoft announces a $19B deal to buy Ubisoft. All future Ubisoft games will launch day-one on Game Pass. Here\'s everything we know.',
        'status': 'publie',
    },
]


class Command(BaseCommand):
    help = 'Seed 10 articles, categories, tags, and games into the database.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        cats = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']},
            )
            cats[cat_data['slug']] = cat
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {cat.name}")

        self.stdout.write('Seeding tags...')
        tags = {}
        for tag_data in TAGS:
            tag, created = Tag.objects.get_or_create(
                slug=tag_data['slug'],
                defaults={'name': tag_data['name'], 'type': tag_data['type']},
            )
            tags[tag_data['slug']] = tag
            self.stdout.write(f"  {'Created' if created else 'Exists'}: {tag.name}")

        source, _ = Source.objects.get_or_create(
            name='GNEWZ Editorial',
            defaults={'type': 'api', 'url': 'https://gnewz.com', 'fetch_interval': 60},
        )

        self.stdout.write('Seeding articles...')
        article_count = 0
        for art_data in ARTICLES:
            slug = slugify(art_data['title'])
            if Article.objects.filter(slug=slug).exists():
                self.stdout.write(f"  Exists: {art_data['title'][:60]}")
                continue

            article = Article.objects.create(
                title=art_data['title'],
                slug=slug,
                content=art_data['content'],
                category=cats.get(art_data['category']),
                source=source,
                status=art_data['status'],
                is_featured=art_data['is_featured'],
                is_breaking=art_data['is_breaking'],
                meta_title=art_data.get('meta_title', ''),
                meta_description=art_data.get('meta_description', ''),
                published_at=timezone.now() if art_data['status'] == 'publie' else None,
            )

            for tag_slug in art_data.get('tags', []):
                if tag_slug in tags:
                    article.tags.add(tags[tag_slug])

            article_count += 1
            self.stdout.write(self.style.SUCCESS(f'  Created: {article.title[:60]}'))

        self.stdout.write('Seeding games...')
        game_count = 0
        esports_cat = cats.get('esports')
        pc_cat = cats.get('pc-gaming')
        console_cat = cats.get('console-gaming')
        indie_cat = cats.get('indie-games')

        game_categories = {
            'Valorant': [esports_cat, pc_cat],
            'Elden Ring': [console_cat, pc_cat],
            'GTA VI': [console_cat],
            'League of Legends': [esports_cat, pc_cat],
            'Hollow Knight: Silksong': [indie_cat, pc_cat],
        }

        for game_data in GAMES:
            game, created = Game.objects.get_or_create(
                slug=slugify(game_data['title']),
                defaults={k: v for k, v in game_data.items() if k != 'title'},
                title=game_data['title'],
            )
            if created:
                for cat in game_categories.get(game_data['title'], []):
                    if cat:
                        game.categories.add(cat)
                game_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created game: {game.title}'))
            else:
                self.stdout.write(f'  Exists: {game.title}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {article_count} articles and {game_count} games created.'
        ))
