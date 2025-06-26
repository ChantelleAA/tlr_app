# management/commands/populate_kg_primary_data.py
from django.core.management.base import BaseCommand
from suggestor.models import (
    ClassLevel, Subject, Theme, KeyLearningArea, CoreCompetency, 
    GoalTag, ResourceType, SpecialNeed, LearningStyle, Material,
    Strand, SubStrand, ContentStandard, Indicator, Tlr
)

class Command(BaseCommand):
    help = 'Populate comprehensive TLR data for KG1, KG2, and Classes 1-3'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive KG and Primary data...')
        
        # Create TLRs for each class level
        self.create_kg1_tlrs()
        self.create_kg2_tlrs()
        self.create_class1_tlrs()
        self.create_class2_tlrs()
        self.create_class3_tlrs()
        self.create_cross_curricular_kg_primary_tlrs()
        
        self.stdout.write(self.style.SUCCESS('KG and Primary TLRs created successfully!'))

    def create_kg1_tlrs(self):
        """Create TLRs for KG1 (4-5 year olds) - Focus on school readiness"""
        kg1 = ClassLevel.objects.get(name="KG1")
        
        # Language and Literacy TLRs for KG1
        lang_subject = Subject.objects.get(class_level=kg1, title="Language and Literacy")
        
        kg1_lang_tlrs = [
            {
                'title': 'Interactive Phonics Sound Box Adventure',
                'brief_description': 'Multi-compartment sound box with objects and cards for each phonics sound, promoting systematic phonics learning.',
                'steps_to_make': '''1. Create compartmentalized box with 26 sections (one per letter)
2. For each letter, include:
   - 3-4 real objects starting with that sound
   - Picture cards showing more examples
   - Action cards showing Jolly Phonics movements
   - Letter formation tracing cards with arrows
3. Add sound recording buttons for each letter
4. Include instruction cards for various games
5. Create assessment check-off sheets''',
                'tips_for_use': '''- Introduce 2-3 sounds per week systematically
- Let children find objects and sort them into correct compartments
- Practice letter formation while saying sounds
- Use for small group rotations and individual practice
- Encourage children to teach sounds to others
- Connect sounds to children\'s names and familiar words''',
                'materials': ['Cardboard boxes', 'Real objects', 'Picture cards', 'Sound buttons', 'Tracing cards', 'Assessment sheets'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify all 26 letter sounds, form letters correctly, and demonstrate phonemic awareness through sorting and blending activities.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner', 'Auditory Learner'],
                'special_needs': ['Speech Delay', 'Attention Difficulties'],
                'themes': ['My School']
            },
            {
                'title': 'Sight Word Building and Reading Center',
                'brief_description': 'Interactive center with moveable letters, word cards, and activities for building and reading common sight words.',
                'steps_to_make': '''1. Create magnetic letter board with colorful backing
2. Design sight word cards with:
   - Target word in large letters
   - Picture clue if applicable
   - Sentence using the word
   - Space for children to build word with magnetic letters
3. Include different difficulty levels (10, 20, 50 sight words)
4. Add word family sorting mats
5. Create sight word bingo games and flash cards
6. Include reading books featuring sight words''',
                'tips_for_use': '''- Start with most common words: the, and, is, it, in
- Practice building words with magnetic letters daily
- Use sight words in context through simple sentences
- Play sight word games during transition times
- Encourage children to spot sight words in books
- Create personal sight word dictionaries for each child''',
                'materials': ['Magnetic letters', 'Word cards', 'Reading books', 'Bingo games', 'Sorting mats', 'Mini dictionaries'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'remember',
                'budget_band': 'medium',
                'learning_outcome': 'Children will recognize and read 25-50 sight words automatically and use them to build simple sentences.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Attention Difficulties', 'Visual Impairment'],
                'themes': ['My School']
            },
            {
                'title': 'Story Sequencing and Comprehension Theater',
                'brief_description': 'Interactive theater with story sequence cards, character puppets, and comprehension activities.',
                'steps_to_make': '''1. Build simple puppet theater from large cardboard box
2. Create story sequence cards for 5-6 familiar stories
3. Design character puppets for each story
4. Make comprehension question cards:
   - Who was in the story?
   - What happened first/next/last?
   - Where did the story happen?
   - How did the character feel?
5. Include story prediction cards and alternative ending suggestions
6. Add story creation spinner with characters, settings, problems''',
                'tips_for_use': '''- Read story first, then use theater to retell
- Let children arrange sequence cards in correct order
- Ask comprehension questions during puppet show
- Encourage children to create new endings
- Use theater for small group reading comprehension
- Have children take turns being "director" and asking questions''',
                'materials': ['Cardboard theater', 'Sequence cards', 'Character puppets', 'Question cards', 'Story spinner', 'Books'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will sequence story events correctly, answer comprehension questions, and demonstrate understanding of story elements.',
                'learning_styles': ['Visual Learner', 'Social Learner', 'Kinesthetic Learner'],
                'special_needs': ['Speech Delay', 'Social Anxiety'],
                'themes': ['My School', 'Festivals and Celebrations']
            }
        ]
        
        for tlr_data in kg1_lang_tlrs:
            self.create_tlr(tlr_data, kg1, lang_subject)

        # Numeracy TLRs for KG1
        num_subject = Subject.objects.get(class_level=kg1, title="Numeracy")
        
        kg1_num_tlrs = [
            {
                'title': 'Number Recognition and Formation Workshop',
                'brief_description': 'Multi-sensory workshop for learning numbers 1-20 with formation practice, counting, and number concepts.',
                'steps_to_make': '''1. Create number formation trays with different textures:
   - Sand trays for finger tracing
   - Playdough mats for forming numbers
   - Textured number cards for tactile exploration
2. Include counting collections for each number (1-20)
3. Add number line activities and games
4. Create "number of the day" investigation cards
5. Include simple addition and subtraction manipulatives
6. Add number recognition assessment tools''',
                'tips_for_use': '''- Practice one number formation daily using different methods
- Count real objects to match written numbers
- Use number line for simple addition (counting on)
- Encourage children to find numbers in environment
- Practice writing numbers in different media
- Connect numbers to real-life situations: ages, addresses, phone numbers''',
                'materials': ['Sand trays', 'Playdough', 'Textured cards', 'Counting objects', 'Number lines', 'Assessment tools'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'remember',
                'budget_band': 'medium',
                'learning_outcome': 'Children will recognize, write, and understand quantities for numbers 1-20, and perform simple addition and subtraction.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Motor Delays', 'Attention Difficulties'],
                'themes': ['My School']
            },
            {
                'title': 'Measurement and Comparison Laboratory',
                'brief_description': 'Hands-on laboratory with tools and activities for exploring length, weight, capacity, and comparison concepts.',
                'steps_to_make': '''1. Set up measurement stations:
   - Length: rulers, measuring tapes, string, blocks
   - Weight: balance scales, various objects to weigh
   - Capacity: containers of different sizes, water, rice
   - Time: clocks, timers, daily schedule cards
2. Create recording sheets for measurements
3. Include comparison vocabulary cards (longer/shorter, heavier/lighter)
4. Add estimation activities and prediction cards
5. Create "Measurement Detective" investigation cards''',
                'tips_for_use': '''- Start with direct comparisons before using tools
- Use consistent vocabulary: long, longer, longest
- Encourage estimation before measuring
- Record findings on simple charts
- Connect measurements to daily activities
- Let children create their own measurement challenges''',
                'materials': ['Measuring tools', 'Balance scales', 'Various containers', 'Recording sheets', 'Comparison cards', 'Investigation cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will compare and measure objects using appropriate tools and vocabulary, and make reasonable estimations.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Motor Delays', 'Developmental Delays'],
                'themes': ['My Environment', 'My School']
            }
        ]
        
        for tlr_data in kg1_num_tlrs:
            self.create_tlr(tlr_data, kg1, num_subject)

    def create_kg2_tlrs(self):
        """Create TLRs for KG2 (5-6 year olds) - Focus on advanced readiness skills"""
        kg2 = ClassLevel.objects.get(name="KG2")
        
        # Language and Literacy TLRs for KG2
        lang_subject = Subject.objects.get(class_level=kg2, title="Language and Literacy")
        
        kg2_lang_tlrs = [
            {
                'title': 'Advanced Phonics Blending and Segmenting Station',
                'brief_description': 'Comprehensive station for blending sounds into words and segmenting words into individual sounds.',
                'steps_to_make': '''1. Create blending slides with consonant-vowel-consonant words
2. Design sound segmenting mats with boxes for each sound
3. Include picture cards for 100+ three-letter words
4. Add progressive difficulty: CVC, CVCC, CCVC words
5. Create self-checking answer keys
6. Include games like "Sound Race" and "Blending Bingo"
7. Add recording sheets for tracking progress''',
                'tips_for_use': '''- Model blending slowly first: /c/ /a/ /t/ = cat
- Use physical movements for each sound
- Progress from blending to segmenting systematically
- Encourage children to use fingers to count sounds
- Connect to spelling and writing activities
- Use nonsense words to test true blending skills''',
                'materials': ['Blending slides', 'Segmenting mats', 'Picture cards', 'Game materials', 'Answer keys', 'Progress sheets'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will blend individual sounds to read simple words and segment words into component sounds for spelling.',
                'learning_styles': ['Auditory Learner', 'Kinesthetic Learner'],
                'special_needs': ['Speech Delay', 'Attention Difficulties'],
                'themes': ['My School']
            },
            {
                'title': 'Independent Reading and Writing Workshop',
                'brief_description': 'Structured workshop with leveled books, writing materials, and guided activities for developing independent literacy skills.',
                'steps_to_make': '''1. Organize books by reading levels (A-D for beginners)
2. Create comfortable reading area with pillows and good lighting
3. Set up writing station with:
   - Various paper types (lined, blank, story templates)
   - Writing tools (pencils, crayons, markers)
   - Word walls and picture dictionaries
   - Story starter prompts
4. Include reading comprehension activities
5. Add peer sharing and presentation area
6. Create individual reading and writing portfolios''',
                'tips_for_use': '''- Start with 10-15 minute independent sessions
- Teach children how to choose "just right" books
- Encourage invented spelling in early writing
- Provide quiet space for concentration
- Conference with individual children regularly
- Celebrate all attempts at reading and writing''',
                'materials': ['Leveled books', 'Writing materials', 'Word walls', 'Story templates', 'Portfolios', 'Comfortable seating'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will read simple books independently and write sentences expressing their ideas using invented and conventional spelling.',
                'learning_styles': ['Visual Learner', 'Solitary Learner'],
                'special_needs': ['Attention Difficulties', 'Social Anxiety'],
                'themes': ['My School', 'All About Me']
            }
        ]
        
        for tlr_data in kg2_lang_tlrs:
            self.create_tlr(tlr_data, kg2, lang_subject)

    def create_class1_tlrs(self):
        """Create TLRs for Class 1 (6-7 year olds) - Focus on foundational academic skills"""
        class1 = ClassLevel.objects.get(name="Class 1")
        
        # English Language TLRs for Class 1
        english_subject = Subject.objects.get(class_level=class1, title="English Language")
        
        class1_english_tlrs = [
            {
                'title': 'Guided Reading Comprehension Center',
                'brief_description': 'Structured center with leveled readers, comprehension strategies, and discussion activities for developing reading skills.',
                'steps_to_make': '''1. Organize books by guided reading levels (E-J)
2. Create comprehension strategy posters:
   - Making connections (text to self, text to world)
   - Predicting and confirming
   - Visualizing
   - Questioning
   - Summarizing
3. Design comprehension activity cards for each book
4. Include vocabulary development activities
5. Create discussion prompt cards for book talks
6. Add reading response journals and graphic organizers''',
                'tips_for_use': '''- Group children by similar reading levels
- Teach one strategy at a time explicitly
- Encourage children to discuss books with partners
- Use graphic organizers to support comprehension
- Connect reading to children\'s experiences
- Celebrate reading growth and achievements''',
                'materials': ['Leveled books', 'Strategy posters', 'Activity cards', 'Response journals', 'Graphic organizers', 'Discussion cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'analyze',
                'budget_band': 'medium',
                'learning_outcome': 'Children will read grade-level texts with comprehension and use strategies to understand and discuss what they read.',
                'learning_styles': ['Visual Learner', 'Social Learner'],
                'special_needs': ['Attention Difficulties', 'Speech Delay'],
                'themes': ['My School', 'My Community']
            },
            {
                'title': 'Grammar and Sentence Construction Workshop',
                'brief_description': 'Interactive workshop for learning parts of speech, sentence structure, and grammar rules through hands-on activities.',
                'steps_to_make': '''1. Create moveable word cards in different colors:
   - Red for nouns
   - Blue for verbs
   - Green for adjectives
   - Yellow for articles (a, an, the)
2. Design sentence building mats with spaces for each part of speech
3. Include grammar sorting activities
4. Add punctuation cards and rules posters
5. Create "Fix the Sentence" error correction activities
6. Include creative writing prompts using target grammar''',
                'tips_for_use': '''- Start with simple noun-verb sentences
- Use color coding consistently for parts of speech
- Encourage children to act out sentences they create
- Practice grammar in context of meaningful writing
- Use games to make grammar learning fun
- Connect to children\'s oral language patterns''',
                'materials': ['Colored word cards', 'Sentence mats', 'Sorting activities', 'Punctuation cards', 'Error correction sheets', 'Writing prompts'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify parts of speech, construct grammatically correct sentences, and apply grammar rules in their writing.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Speech Delay', 'Attention Difficulties'],
                'themes': ['My School']
            }
        ]
        
        for tlr_data in class1_english_tlrs:
            self.create_tlr(tlr_data, class1, english_subject)

        # Mathematics TLRs for Class 1
        math_subject = Subject.objects.get(class_level=class1, title="Mathematics")
        
        class1_math_tlrs = [
            {
                'title': 'Place Value and Number Sense Exploration',
                'brief_description': 'Comprehensive materials for understanding place value, number relationships, and number sense up to 100.',
                'steps_to_make': '''1. Create base-10 blocks using different materials:
   - Units: small cubes or beans
   - Tens: rods or bundled sticks
   - Hundreds: flat squares or plates
2. Design place value charts and mats
3. Include number line activities (0-100)
4. Create "What Number Am I?" riddle cards
5. Add number comparison activities (>, <, =)
6. Include estimation jars with different quantities''',
                'tips_for_use': '''- Use concrete manipulatives before abstract numbers
- Practice bundling and unbundling activities daily
- Connect place value to money concepts
- Use number line for counting patterns
- Encourage estimation before counting
- Relate to real-world examples: house numbers, ages''',
                'materials': ['Base-10 blocks', 'Place value charts', 'Number lines', 'Riddle cards', 'Comparison symbols', 'Estimation jars'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will understand place value concepts, compare numbers to 100, and demonstrate strong number sense.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Attention Difficulties', 'Developmental Delays'],
                'themes': ['My Environment']
            },
            {
                'title': 'Addition and Subtraction Strategy Center',
                'brief_description': 'Multi-strategy center for learning various approaches to addition and subtraction within 20.',
                'steps_to_make': '''1. Create strategy station posters:
   - Counting on/back
   - Using doubles
   - Making 10
   - Fact families
   - Number line jumps
2. Include manipulatives for each strategy
3. Design problem-solving task cards
4. Add games for fact fluency practice
5. Create assessment tools for strategy understanding
6. Include real-world word problem scenarios''',
                'tips_for_use': '''- Teach strategies explicitly, one at a time
- Allow children to choose strategies that work for them
- Use story problems to make math meaningful
- Practice fact fluency daily in short sessions
- Connect to money and measurement problems
- Encourage explaining mathematical thinking''',
                'materials': ['Strategy posters', 'Manipulatives', 'Task cards', 'Math games', 'Assessment tools', 'Word problems'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will use multiple strategies to solve addition and subtraction problems within 20 and explain their mathematical thinking.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Attention Difficulties', 'Motor Delays'],
                'themes': ['My Environment', 'My Community']
            }
        ]
        
        for tlr_data in class1_math_tlrs:
            self.create_tlr(tlr_data, class1, math_subject)

    def create_class2_tlrs(self):
        """Create TLRs for Class 2 (7-8 year olds) - Focus on developing fluency and deeper understanding"""
        class2 = ClassLevel.objects.get(name="Class 2")
        
        # English Language TLRs for Class 2
        english_subject = Subject.objects.get(class_level=class2, title="English Language")
        
        class2_english_tlrs = [
            {
                'title': 'Advanced Reading Fluency and Expression Center',
                'brief_description': 'Center focused on developing reading fluency, expression, and advanced comprehension skills.',
                'steps_to_make': '''1. Create fluency practice materials:
   - Repeated reading passages at various levels
   - Expression and intonation practice scripts
   - Partner reading protocols
   - Reading rate tracking charts
2. Include comprehension deepening activities:
   - Character analysis templates
   - Plot mapping organizers
   - Theme exploration cards
   - Author\'s purpose activities
3. Add oral presentation and performance opportunities
4. Create listening center with recorded texts''',
                'tips_for_use': '''- Model fluent reading daily
- Practice repeated reading with partners
- Focus on expression and meaning, not just speed
- Use reader\'s theater for expression practice
- Encourage children to self-assess fluency
- Connect fluency to comprehension improvement''',
                'materials': ['Reading passages', 'Expression scripts', 'Tracking charts', 'Analysis templates', 'Recording equipment', 'Performance props'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'analyze',
                'budget_band': 'medium',
                'learning_outcome': 'Children will read grade-level texts fluently with expression and demonstrate deep comprehension through analysis and discussion.',
                'learning_styles': ['Auditory Learner', 'Visual Learner', 'Social Learner'],
                'special_needs': ['Speech Delay', 'Social Anxiety'],
                'themes': ['My Community', 'Festivals and Celebrations']
            },
            {
                'title': 'Creative Writing and Publishing Workshop',
                'brief_description': 'Complete writing workshop with planning tools, revision strategies, and publishing opportunities.',
                'steps_to_make': '''1. Set up writing process stations:
   - Planning: graphic organizers, story maps, idea webs
   - Drafting: various paper types, writing tools
   - Revising: editing checklists, peer review forms
   - Publishing: book-making materials, illustration supplies
2. Create genre-specific writing guides
3. Include mentor texts for each writing type
4. Add writing conference forms and rubrics
5. Set up author\'s chair and celebration area
6. Create class anthology and individual portfolios''',
                'tips_for_use': '''- Teach the writing process explicitly
- Conference with individual writers regularly
- Encourage risk-taking and creativity
- Celebrate all stages of writing, not just final products
- Use mentor texts to inspire and instruct
- Create authentic audiences for children\'s writing''',
                'materials': ['Graphic organizers', 'Writing tools', 'Editing materials', 'Book-making supplies', 'Mentor texts', 'Portfolio folders'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will write in various genres using the writing process and publish their work for authentic audiences.',
                'learning_styles': ['Visual Learner', 'Solitary Learner', 'Social Learner'],
                'special_needs': ['Attention Difficulties', 'Motor Delays'],
                'themes': ['All About Me', 'My Community']
            }
        ]
        
        for tlr_data in class2_english_tlrs:
            self.create_tlr(tlr_data, class2, english_subject)

    def create_class3_tlrs(self):
        """Create TLRs for Class 3 (8-9 year olds) - Focus on advanced skills and independence"""
        class3 = ClassLevel.objects.get(name="Class 3")
        
        # English Language TLRs for Class 3
        english_subject = Subject.objects.get(class_level=class3, title="English Language")
        
        class3_english_tlrs = [
            {
                'title': 'Literature Circle Discussion and Analysis Center',
                'brief_description': 'Sophisticated center for book discussions, literary analysis, and critical thinking about texts.',
                'steps_to_make': '''1. Create role cards for literature circles:
   - Discussion Director: prepares questions
   - Vocabulary Enricher: finds interesting words
   - Illustrator: creates visual responses
   - Connector: makes text-to-life connections
   - Summarizer: retells important parts
2. Design analysis templates for different genres
3. Include critical thinking question prompts
4. Add multimedia response options
5. Create peer evaluation forms
6. Set up presentation and sharing protocols''',
                'tips_for_use': '''- Start with shorter texts and simple roles
- Model each role before independent practice
- Encourage deep thinking and analysis
- Rotate roles so children experience all perspectives
- Connect discussions to writing and other subjects
- Celebrate insights and different interpretations''',
                'materials': ['Role cards', 'Analysis templates', 'Question prompts', 'Response materials', 'Evaluation forms', 'Presentation tools'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'evaluate',
                'budget_band': 'medium',
                'learning_outcome': 'Children will engage in sophisticated discussions about literature, analyze texts critically, and express well-reasoned opinions.',
                'learning_styles': ['Social Learner', 'Visual Learner', 'Auditory Learner'],
                'special_needs': ['Social Anxiety', 'Speech Delay'],
                'themes': ['My Community', 'Our Values']
            },
            {
                'title': 'Advanced Research and Presentation Project Center',
                'brief_description': 'Complete research center with information gathering tools, organization systems, and presentation resources.',
                'steps_to_make': '''1. Create research process guides:
   - Question formulation templates
   - Source evaluation checklists
   - Note-taking organizers
   - Citation format examples
2. Include information gathering tools:
   - Interview question templates
   - Survey forms
   - Observation sheets
   - Digital research guidelines
3. Add presentation format options:
   - Poster templates
   - Slideshow guidelines
   - Demonstration planning sheets
   - Video creation tools
4. Include assessment rubrics and self-evaluation forms''',
                'tips_for_use': '''- Start with topics of high interest to children
- Teach research skills systematically
- Provide multiple sources and formats
- Encourage collaboration and peer learning
- Focus on process as much as final product
- Connect research to real-world issues and problems''',
                'materials': ['Research guides', 'Organization tools', 'Source materials', 'Presentation supplies', 'Technology tools', 'Assessment forms'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will conduct independent research, organize information effectively, and present findings to authentic audiences.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner', 'Social Learner'],
                'special_needs': ['Attention Difficulties', 'Social Anxiety'],
                'themes': ['My Community', 'Our Values', 'My Nation']
            }
        ]
        
        for tlr_data in class3_english_tlrs:
            self.create_tlr(tlr_data, class3, english_subject)

        # Mathematics TLRs for Class 3
        math_subject = Subject.objects.get(class_level=class3, title="Mathematics")
        
        class3_math_tlrs = [
            {
                'title': 'Multi-Step Problem Solving and Strategy Center',
                'brief_description': 'Advanced center for solving complex word problems using multiple strategies and mathematical reasoning.',
                'steps_to_make': '''1. Create problem-solving strategy posters:
   - Understand the problem
   - Devise a plan
   - Carry out the plan
   - Look back and check
2. Include various problem types:
   - Multi-step word problems
   - Open-ended investigations
   - Real-world applications
   - Logic and reasoning puzzles
3. Add strategy tools and manipulatives
4. Create reflection and explanation templates
5. Include peer collaboration protocols
6. Add assessment rubrics for problem-solving process''',
                'tips_for_use': '''- Teach problem-solving strategies explicitly
- Encourage multiple solution methods
- Focus on mathematical reasoning and explanation
- Use real-world contexts whenever possible
- Promote collaboration and mathematical discourse
- Celebrate creative thinking and persistence''',
                'materials': ['Strategy posters', 'Problem sets', 'Manipulatives', 'Reflection templates', 'Collaboration tools', 'Assessment rubrics'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'evaluate',
                'budget_band': 'medium',
                'learning_outcome': 'Children will solve multi-step problems using various strategies, explain their mathematical reasoning, and evaluate solution methods.',
                'learning_styles': ['Visual Learner', 'Social Learner', 'Kinesthetic Learner'],
                'special_needs': ['Attention Difficulties', 'Developmental Delays'],
                'themes': ['My Community', 'My Environment']
            },
            {
                'title': 'Fraction and Decimal Exploration Laboratory',
                'brief_description': 'Hands-on laboratory for understanding fractions, decimals, and their real-world applications.',
                'steps_to_make': '''1. Create fraction manipulation materials:
   - Fraction circles, bars, and squares
   - Pizza and chocolate bar fraction models
   - Fraction number lines
   - Equivalent fraction matching games
2. Include decimal exploration tools:
   - Base-10 blocks for decimal representation
   - Decimal place value charts
   - Money models for decimal understanding
   - Measurement tools showing decimal increments
3. Add real-world application activities:
   - Cooking measurement conversions
   - Sports statistics analysis
   - Shopping and money problems
4. Create assessment and progress tracking tools''',
                'tips_for_use': '''- Start with concrete fraction models before symbols
- Connect fractions to familiar experiences (sharing food)
- Use multiple representations for same concept
- Relate decimals to money and measurement
- Encourage estimation and reasoning
- Make connections between fractions and decimals explicit''',
                'materials': ['Fraction models', 'Decimal tools', 'Place value charts', 'Real objects', 'Measurement tools', 'Assessment sheets'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will understand fraction and decimal concepts, make connections between different representations, and apply concepts to real situations.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Attention Difficulties', 'Motor Delays'],
                'themes': ['Food and Nutrition', 'My Community']
            }
        ]
        
        for tlr_data in class3_math_tlrs:
            self.create_tlr(tlr_data, class3, math_subject)

        # Science TLRs for Class 3
        science_subject = Subject.objects.get(class_level=class3, title="Science")
        
        class3_science_tlrs = [
            {
                'title': 'Scientific Investigation and Experiment Station',
                'brief_description': 'Complete laboratory setup for conducting scientific investigations, making observations, and recording findings.',
                'steps_to_make': '''1. Set up investigation tools:
   - Magnifying glasses and microscopes
   - Measuring tools (rulers, scales, thermometers)
   - Collection containers and observation trays
   - Safety equipment (goggles, gloves)
2. Create investigation protocol cards:
   - Question formation guides
   - Hypothesis templates
   - Observation recording sheets
   - Conclusion drawing frameworks
3. Include experiment activity cards for:
   - Plant growth investigations
   - Simple chemistry reactions
   - Physics explorations (magnets, forces)
   - Weather and climate studies
4. Add scientific vocabulary development materials''',
                'tips_for_use': '''- Model scientific thinking and questioning
- Encourage predictions before investigations
- Emphasize careful observation and recording
- Discuss findings and draw evidence-based conclusions
- Connect investigations to real-world phenomena
- Celebrate curiosity and scientific thinking''',
                'materials': ['Scientific tools', 'Investigation cards', 'Recording sheets', 'Safety equipment', 'Experiment supplies', 'Vocabulary materials'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'analyze',
                'budget_band': 'medium',
                'learning_outcome': 'Children will conduct scientific investigations, make careful observations, record data, and draw evidence-based conclusions.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner', 'Nature Learner'],
                'special_needs': ['Attention Difficulties', 'Sensory Processing'],
                'themes': ['Plants and Nature', 'My Environment', 'Weather and Seasons']
            }
        ]
        
        for tlr_data in class3_science_tlrs:
            self.create_tlr(tlr_data, class3, science_subject)

    def create_cross_curricular_kg_primary_tlrs(self):
        """Create cross-curricular TLRs that span multiple subjects and age groups"""
        
        # Get all class levels
        kg1 = ClassLevel.objects.get(name="KG1")
        kg2 = ClassLevel.objects.get(name="KG2")
        class1 = ClassLevel.objects.get(name="Class 1")
        class2 = ClassLevel.objects.get(name="Class 2")
        class3 = ClassLevel.objects.get(name="Class 3")
        
        # Cross-curricular TLRs that can be adapted for different levels
        cross_curricular_tlrs = [
            {
                'title': 'Ghanaian Cultural Heritage Interactive Museum',
                'brief_description': 'Classroom museum featuring Ghanaian traditions, artifacts, and cultural practices for all age groups.',
                'class_level': kg1,
                'subject': 'Our World Our People',
                'steps_to_make': '''1. Create museum sections:
   - Traditional clothing display with dress-up opportunities
   - Musical instruments from different regions
   - Traditional games and toys
   - Food and cooking utensils
   - Art and craft examples
   - Language and storytelling corner
2. Include interactive elements:
   - Audio recordings of traditional music
   - Hands-on craft activities
   - Role-play scenarios
   - Storytelling props and costumes
3. Add guided tour materials and information cards
4. Create visitor response and reflection activities''',
                'tips_for_use': '''- Invite community elders to share stories and knowledge
- Encourage children to bring family artifacts
- Connect to current events and celebrations
- Use museum for dramatic play and role-playing
- Adapt complexity for different age groups
- Create connections to other subject areas''',
                'materials': ['Cultural artifacts', 'Display materials', 'Audio equipment', 'Craft supplies', 'Costumes', 'Information cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'large',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will develop appreciation for Ghanaian culture, understand cultural diversity, and make connections to their own heritage.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner', 'Social Learner'],
                'special_needs': ['Social Anxiety', 'Cultural Integration'],
                'themes': ['My Community', 'My Nation', 'Festivals and Celebrations']
            },
            {
                'title': 'Environmental Conservation Action Center',
                'brief_description': 'Interactive center focused on environmental awareness, conservation practices, and community action.',
                'class_level': class2,
                'subject': 'Science',
                'steps_to_make': '''1. Set up conservation investigation stations:
   - Water conservation experiments
   - Recycling sorting and processing
   - Energy usage monitoring
   - Waste reduction challenges
2. Create action planning materials:
   - Environmental problem identification sheets
   - Solution brainstorming templates
   - Action plan organizers
   - Community presentation tools
3. Include monitoring and tracking systems:
   - Conservation behavior charts
   - Environmental impact measurements
   - Progress documentation materials
4. Add real-world connection opportunities''',
                'tips_for_use': '''- Start with school environment before expanding to community
- Encourage real action, not just discussion
- Connect to family and community practices
- Use data collection and analysis
- Celebrate environmental achievements
- Invite environmental experts to share knowledge''',
                'materials': ['Investigation tools', 'Monitoring equipment', 'Planning templates', 'Presentation materials', 'Action tracking sheets', 'Community resources'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will understand environmental issues, develop conservation practices, and take action to protect their environment.',
                'learning_styles': ['Kinesthetic Learner', 'Nature Learner', 'Social Learner'],
                'special_needs': ['Attention Difficulties'],
                'themes': ['My Environment', 'Plants and Nature', 'My Community']
            }
        ]
        
        for tlr_data in cross_curricular_tlrs:
            class_level = tlr_data['class_level']
            subject = Subject.objects.get(class_level=class_level, title=tlr_data['subject'])
            self.create_tlr(tlr_data, class_level, subject)

    def create_tlr(self, tlr_data, class_level, subject):
        """Helper method to create TLR objects with all relationships"""
        
        # Create the main TLR object
        tlr, created = Tlr.objects.get_or_create(
            title=tlr_data['title'],
            defaults={
                'class_level': class_level,
                'subject': subject,
                'term': 1,
                'brief_description': tlr_data['brief_description'],
                'steps_to_make': tlr_data['steps_to_make'],
                'tips_for_use': tlr_data['tips_for_use'],
                'time_needed': tlr_data['time_needed'],
                'intended_use': tlr_data['intended_use'],
                'tlr_type': tlr_data['tlr_type'],
                'class_size': tlr_data['class_size'],
                'bloom_level': tlr_data['bloom_level'],
                'budget_band': tlr_data['budget_band'],
                'learning_outcome': tlr_data['learning_outcome'],
                'is_published': True,
                'slug': tlr_data['title'].lower().replace(' ', '-').replace('\'', '')
            }
        )
        
        if created:
            # Add materials
            for material_name in tlr_data['materials']:
                try:
                    material = Material.objects.get(name=material_name)
                    tlr.materials.add(material)
                except Material.DoesNotExist:
                    self.stdout.write(f'Warning: Material "{material_name}" not found')
            
            # Add learning styles
            for style_name in tlr_data['learning_styles']:
                try:
                    style = LearningStyle.objects.get(name=style_name)
                    tlr.learning_styles.add(style)
                except LearningStyle.DoesNotExist:
                    self.stdout.write(f'Warning: Learning style "{style_name}" not found')
            
            # Add special needs if specified
            if 'special_needs' in tlr_data:
                for need_name in tlr_data['special_needs']:
                    try:
                        need = SpecialNeed.objects.get(name=need_name)
                        tlr.special_needs.add(need)
                    except SpecialNeed.DoesNotExist:
                        self.stdout.write(f'Warning: Special need "{need_name}" not found')
            
            # Add themes
            for theme_name in tlr_data['themes']:
                try:
                    theme = Theme.objects.get(title=theme_name)
                    tlr.themes.add(theme)
                except Theme.DoesNotExist:
                    self.stdout.write(f'Warning: Theme "{theme_name}" not found')
            
            self.stdout.write(f'Created TLR: {tlr.title}')
        else:
            self.stdout.write(f'TLR already exists: {tlr.title}')