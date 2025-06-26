# management/commands/populate_nursery_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from suggestor.models import (
    ClassLevel, Subject, Theme, KeyLearningArea, CoreCompetency, 
    GoalTag, ResourceType, SpecialNeed, LearningStyle, Material,
    Strand, SubStrand, ContentStandard, Indicator, Tlr
)

class Command(BaseCommand):
    help = 'Populate comprehensive nursery-level TLR data based on early childhood development'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive nursery data...')
        
        # Create foundational data
        self.create_class_levels_and_subjects()
        self.create_themes()
        self.create_key_learning_areas()
        self.create_core_competencies()
        self.create_goal_tags()
        self.create_resource_types()
        self.create_special_needs()
        self.create_learning_styles()
        self.create_materials()
        
        # Create curriculum structure
        self.create_nursery_curriculum()
        
        # Create comprehensive TLRs
        self.create_language_literacy_tlrs()
        self.create_numeracy_tlrs()
        self.create_creative_arts_tlrs()
        self.create_environmental_studies_tlrs()
        self.create_physical_development_tlrs()
        self.create_music_movement_tlrs()
        self.create_additional_comprehensive_tlrs()
        
        self.stdout.write(self.style.SUCCESS('Comprehensive nursery data created successfully!'))

    def create_class_levels_and_subjects(self):
        # Early childhood class levels
        class_data = [
            ("1", "Creche", ["Language and Literacy", "Numeracy", "Creative Arts", "Environmental Studies", "Physical Development", "Music and Movement"]),
            ("2", "Nursery", ["Language and Literacy", "Numeracy", "Creative Arts", "Environmental Studies", "Physical Development", "Music and Movement"]),
            ("3", "KG1", ["Language and Literacy", "Numeracy", "Our World Our People", "Creative Arts", "Physical Development", "Religious and Moral Education"]),
            ("4", "KG2", ["Language and Literacy", "Numeracy", "Our World Our People", "Creative Arts", "Physical Development", "Religious and Moral Education"])
        ]

        for code, name, subjects in class_data:
            cl, created = ClassLevel.objects.get_or_create(code=code, defaults={'name': name})
            if created:
                self.stdout.write(f'Created class level: {name}')
            
            for subject_title in subjects:
                subj, created = Subject.objects.get_or_create(class_level=cl, title=subject_title)
                if created:
                    self.stdout.write(f'  Created subject: {subject_title}')

    def create_themes(self):
        themes = [
            "All About Me", "My Family", "My Body", "My Feelings", 
            "My Home", "My School", "Animals Around Me", "Plants and Nature",
            "Weather and Seasons", "Community Helpers", "Transportation",
            "Food and Nutrition", "Safety", "Festivals and Celebrations"
        ]
        for theme in themes:
            obj, created = Theme.objects.get_or_create(title=theme)
            if created:
                self.stdout.write(f'Created theme: {theme}')

    def create_key_learning_areas(self):
        klas = [
            "Language Development", "Pre-Math Skills", "Social-Emotional Development", 
            "Physical Motor Skills", "Creative Expression", "Scientific Thinking",
            "Cultural Awareness", "Life Skills"
        ]
        for kla in klas:
            obj, created = KeyLearningArea.objects.get_or_create(title=kla)
            if created:
                self.stdout.write(f'Created KLA: {kla}')

    def create_core_competencies(self):
        competencies = [
            "Communication", "Problem Solving", "Self-Expression", 
            "Social Interaction", "Motor Coordination", "Observation Skills",
            "Following Instructions", "Independence"
        ]
        for comp in competencies:
            obj, created = CoreCompetency.objects.get_or_create(title=comp)
            if created:
                self.stdout.write(f'Created competency: {comp}')

    def create_goal_tags(self):
        goals = ["Introduce", "Practice", "Reinforce", "Assess", "Review", "Extend"]
        for goal in goals:
            obj, created = GoalTag.objects.get_or_create(title=goal)
            if created:
                self.stdout.write(f'Created goal tag: {goal}')

    def create_resource_types(self):
        types = [
            "Sensory Materials", "Picture Cards", "Story Props", "Manipulatives", 
            "Art Supplies", "Musical Instruments", "Puzzles", "Building Blocks",
            "Dress-up Items", "Nature Materials", "Interactive Charts", "Game Materials"
        ]
        for rt in types:
            obj, created = ResourceType.objects.get_or_create(title=rt)
            if created:
                self.stdout.write(f'Created resource type: {rt}')

    def create_special_needs(self):
        needs = [
            ("Speech Delay", "Children who need extra support with verbal communication"),
            ("Sensory Processing", "Children who are over or under-sensitive to sensory input"),
            ("Attention Difficulties", "Children who have trouble focusing or sitting still"),
            ("Motor Delays", "Children who need extra support with physical movements"),
            ("Social Anxiety", "Children who are very shy or have difficulty with social interactions"),
            ("Hearing Impairment", "Children with partial or complete hearing loss"),
            ("Visual Impairment", "Children with vision difficulties"),
            ("Developmental Delays", "Children who may be developing more slowly in various areas")
        ]
        for name, desc in needs:
            obj, created = SpecialNeed.objects.get_or_create(name=name, defaults={"description": desc})
            if created:
                self.stdout.write(f'Created special need: {name}')

    def create_learning_styles(self):
        styles = [
            ("Visual Learner", "Learns best through pictures, colors, and visual demonstrations"),
            ("Auditory Learner", "Learns best through songs, stories, and verbal instructions"),
            ("Kinesthetic Learner", "Learns best through movement, touch, and hands-on activities"),
            ("Social Learner", "Learns best in group settings and through interaction with others"),
            ("Solitary Learner", "Learns best in quiet, individual settings"),
            ("Nature Learner", "Learns best through outdoor activities and natural materials")
        ]
        for name, desc in styles:
            obj, created = LearningStyle.objects.get_or_create(name=name, defaults={"description": desc})
            if created:
                self.stdout.write(f'Created learning style: {name}')

    def create_materials(self):
        materials = [
            # Basic craft materials
            "EVA foam sheet", "Glitter EVA foam sheet", "Pipe cleaners", "Double sided tape", 
            "Paper glue", "Glue sticks", "Cartridge paper", "A4 sheets", "Manila cards", 
            "Coloured sheets", "Crepe paper", "Markers", "Washable markers", "Pencils", 
            "Crayons", "Paints", "Finger paints", "Paintbrushes", "Rulers", "Safety scissors",
            
            # Specialized tools
            "Craft punches", "Punch outs", "Cricut machine",
            
            # Recyclable materials
            "Cardboard boxes", "Empty cereal boxes", "Toilet paper rolls", "Empty tissue rolls",
            "Plastic bottles", "Bottle caps", "Plastic lids", "Egg cartons", "Yogurt containers", 
            "Small plastic containers", "Paper plates", "Plastic spoons", "Old newspapers", 
            "Magazines", "Straws",
            
            # Natural and sensory materials
            "Leaves", "Stones", "Shells", "Twigs", "Seeds", "Flowers", "Feathers", 
            "Sand", "Rice", "Beans", "Water", "Cotton balls", "Cotton wool", "Sponge pieces",
            
            # Fabric and textiles
            "Felt pieces", "Fabric scraps", "Scrap fabric", "Kente offcuts", "Yarn", "Wool", 
            "Ribbon", "Buttons", "Beads", "Popsicle sticks", "Craft sticks",
            
            # Storage and organization
            "Ziploc bags", "Small containers", "Transparent sheets", "Laminating pouches", 
            "Clear contact paper", "Velcro strips", "Velcro dots",
            
            # Educational materials
            "Alphabet cards", "Number cards", "Picture books", "Puzzles", "Building blocks",
            "Counting bears", "Shape cutouts", "Color wheels", "Small mirrors", "Acrylic mirrors",
            "Magnifying glasses", "Printed images", "Stickers", "Mini pegs", "Clothespins",
            
            # Art and decoration
            "Googly eyes", "Foil paper", "Metallic sheets", "Embossed papers", "Textured papers",
            "Masking tape", "Washi tape", "Balloons", "Chalk", "Mini blackboards", "Styrofoam",
            
            # Music and movement
            "Shakers", "Drums", "Bells", "Scarves", "Bean bags", "Hula hoops", "Balls"
        ]
        for material in materials:
            obj, created = Material.objects.get_or_create(name=material)
            if created:
                self.stdout.write(f'Created material: {material}')

    def create_nursery_curriculum(self):
        nursery = ClassLevel.objects.get(name="Nursery")
        
        # Language and Literacy Strands
        lang_subject = Subject.objects.get(class_level=nursery, title="Language and Literacy")
        
        strands = [
            ("Listening and Speaking", ["Vocabulary Building", "Story Comprehension", "Following Instructions"]),
            ("Pre-Reading Skills", ["Letter Recognition", "Phonemic Awareness", "Print Awareness"]),
            ("Pre-Writing Skills", ["Fine Motor Development", "Mark Making", "Shape Recognition"])
        ]
        
        for strand_title, substrands in strands:
            strand, created = Strand.objects.get_or_create(
                class_level=nursery,
                subject=lang_subject,
                term=1,
                title=strand_title,
                defaults={'slug': strand_title.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Created strand: {strand_title}')
                
            for substrand_title in substrands:
                substrand, created = SubStrand.objects.get_or_create(
                    strand=strand,
                    title=substrand_title,
                    defaults={'slug': substrand_title.lower().replace(' ', '-')}
                )
                if created:
                    self.stdout.write(f'  Created substrand: {substrand_title}')

    def create_language_literacy_tlrs(self):
        nursery = ClassLevel.objects.get(name="Nursery")
        lang_subject = Subject.objects.get(class_level=nursery, title="Language and Literacy")
        
        tlrs = [
            {
                'title': 'Animal Sound Matching Cards',
                'brief_description': 'Picture cards featuring farm animals with corresponding sound words to develop phonemic awareness and vocabulary.',
                'steps_to_make': '''1. Print or draw pictures of 10 common animals (cow, sheep, duck, pig, cat, dog, chicken, horse, bee, bird)
2. Create separate cards with sound words (moo, baa, quack, oink, meow, woof, cluck, neigh, buzz, tweet)
3. Laminate all cards for durability
4. Store in a colorful container or bag''',
                'tips_for_use': '''- Start with 3-4 familiar animals, gradually add more
- Make the sounds yourself first, then encourage children to join in
- Play memory games: "What sound does the cow make?"
- Use during circle time or small group activities
- Encourage children to act out the animals while making sounds''',
                'materials': ['Colored paper', 'Washable markers', 'Safety scissors', 'Non-toxic glue'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'flashcard',
                'class_size': 'small',
                'bloom_level': 'remember',
                'budget_band': 'low',
                'learning_outcome': 'Children will identify 6-8 animal sounds and match them to corresponding animals, developing phonemic awareness and vocabulary.',
                'learning_styles': ['Auditory Learner', 'Visual Learner'],
                'special_needs': ['Speech Delay'],
                'themes': ['Animals Around Me']
            },
            {
                'title': 'My Name Recognition Puzzle',
                'brief_description': 'Personalized puzzles featuring each child\'s name to promote letter recognition and self-identity.',
                'steps_to_make': '''1. Write each child's name in large, clear letters on cardboard
2. Decorate around the name with pictures representing the child (favorite color, animal, etc.)
3. Cut between each letter to create puzzle pieces
4. Store each puzzle in a labeled envelope or bag
5. Consider making extras for children with longer names''',
                'tips_for_use': '''- Start by showing the completed puzzle, then mixing pieces
- Help children identify the first letter of their name
- Encourage children to trace letters with their finger
- Use during arrival time as a settling activity
- Create group activities where children help each other''',
                'materials': ['Cardboard', 'Washable markers', 'Safety scissors', 'Colored paper'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'understand',
                'budget_band': 'low',
                'learning_outcome': 'Children will recognize their own name in print and identify at least the first letter of their name.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Attention Difficulties'],
                'themes': ['All About Me']
            },
            {
                'title': 'Story Retelling Props Bag',
                'brief_description': 'Collection of simple props to help children retell familiar stories and develop narrative skills.',
                'steps_to_make': '''1. Choose 3-4 simple stories (Three Little Pigs, Goldilocks, etc.)
2. Create or collect simple props for each story:
   - Three Little Pigs: 3 small houses (straw, sticks, brick), pig and wolf figures
   - Goldilocks: 3 bowls, 3 chairs, 3 beds (different sizes), girl and bear figures
3. Store each story's props in a separate bag with the book
4. Include picture sequence cards showing story events''',
                'tips_for_use': '''- Read the story first, then bring out props
- Encourage children to use props while you retell the story
- Let children take turns using different props
- Ask simple questions: "What happened next?" "How did the pig feel?"
- Allow creative variations of the familiar stories''',
                'materials': ['Fabric scraps', 'Cardboard', 'Picture books', 'Small containers'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will retell simple stories using props and demonstrate understanding of story sequence.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner', 'Social Learner'],
                'special_needs': ['Speech Delay', 'Social Anxiety'],
                'themes': ['My School']
            }
        ]
        
        for tlr_data in tlrs:
            self.create_tlr(tlr_data, nursery, lang_subject)

    def create_numeracy_tlrs(self):
        nursery = ClassLevel.objects.get(name="Nursery")
        num_subject = Subject.objects.get(class_level=nursery, title="Numeracy")
        
        tlrs = [
            {
                'title': 'Counting Teddy Bears in Cups',
                'brief_description': 'Small teddy bear counters and numbered cups for hands-on counting practice from 1-5.',
                'steps_to_make': '''1. Collect or purchase 15 small teddy bear counters
2. Decorate 5 plastic cups with numbers 1-5
3. Add corresponding dot patterns under each number
4. Create instruction cards showing how many bears go in each cup
5. Store all materials in a basket''',
                'tips_for_use': '''- Start with cups 1-3, gradually add 4 and 5
- Count aloud together as children place bears
- Encourage one-to-one correspondence
- Ask "How many bears are in cup number 3?"
- Let children check their work by counting again''',
                'materials': ['Counting bears', 'Plastic bottles', 'Washable markers', 'Number cards'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'low',
                'learning_outcome': 'Children will count objects 1-5 with one-to-one correspondence and recognize written numerals 1-5.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Attention Difficulties', 'Motor Delays'],
                'themes': ['All About Me']
            },
            {
                'title': 'Shape Hunt Discovery Bags',
                'brief_description': 'Fabric bags containing real objects in basic shapes for tactile shape recognition.',
                'steps_to_make': '''1. Create 4 fabric bags in different colors
2. Label each bag with a shape (circle, square, triangle, rectangle)
3. Fill bags with real objects:
   - Circle bag: buttons, coins, bottle caps, rings
   - Square bag: blocks, crackers, small books, tiles
   - Triangle bag: triangular blocks, cut sandwiches, musical triangles
   - Rectangle bag: phones, cards, books, erasers''',
                'tips_for_use': '''- Let children feel objects without looking first
- Ask "What shape do you think this is?"
- Take objects out and name the shape together
- Compare objects: "How are these the same?"
- Go on shape hunts around the classroom''',
                'materials': ['Fabric scraps', 'Buttons', 'Building blocks', 'Shape cutouts'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'understand',
                'budget_band': 'low',
                'learning_outcome': 'Children will identify and name 4 basic shapes through tactile exploration and visual recognition.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Visual Impairment', 'Sensory Processing'],
                'themes': ['My School']
            },
            {
                'title': 'Big and Small Sorting Baskets',
                'brief_description': 'Collection of paired objects in different sizes to teach size comparison and sorting skills.',
                'steps_to_make': '''1. Collect pairs of objects in two sizes:
   - Big and small balls, spoons, cups, books, shoes, hats, boxes
2. Create two labeled baskets: "BIG" and "SMALL" with picture symbols
3. Include measuring tools: large and small containers, string pieces
4. Add picture cards showing big and small comparisons''',
                'tips_for_use': '''- Start with very obvious size differences
- Use comparison language: "This ball is bigger than that ball"
- Let children physically compare by holding objects
- Encourage children to explain their sorting choices
- Connect to children's experiences: "big like daddy, small like baby"''',
                'materials': ['Small containers', 'Balls', 'Picture books', 'Measuring tools'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'analyze',
                'budget_band': 'low',
                'learning_outcome': 'Children will compare objects by size using terms big/small and sort objects into size categories.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Developmental Delays', 'Attention Difficulties'],
                'themes': ['My Home']
            }
        ]
        
        for tlr_data in tlrs:
            self.create_tlr(tlr_data, nursery, num_subject)

    def create_creative_arts_tlrs(self):
        nursery = ClassLevel.objects.get(name="Nursery")
        arts_subject = Subject.objects.get(class_level=nursery, title="Creative Arts")
        
        tlrs = [
            {
                'title': 'Nature Collage Creation Station',
                'brief_description': 'Outdoor collection of natural materials for creating seasonal collages and exploring textures.',
                'steps_to_make': '''1. Set up collection containers for nature walks
2. Gather diverse natural materials: leaves, flowers, twigs, seeds, stones, feathers
3. Prepare large cardboard bases for collages
4. Create texture exploration trays
5. Set up drying area for finished artwork''',
                'tips_for_use': '''- Take children on nature walks to collect materials together
- Encourage touching and describing textures
- Ask open questions: "What does this feel like?" "What colors do you see?"
- Allow free exploration without predetermined outcomes
- Display finished work to celebrate creativity''',
                'materials': ['Leaves', 'Stones', 'Twigs', 'Non-toxic glue', 'Cardboard'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'none',
                'learning_outcome': 'Children will explore natural textures, create original artwork, and develop fine motor skills through collage making.',
                'learning_styles': ['Kinesthetic Learner', 'Nature Learner', 'Visual Learner'],
                'special_needs': ['Sensory Processing', 'Motor Delays'],
                'themes': ['Plants and Nature', 'Weather and Seasons']
            },
            {
                'title': 'Emotion Expression Masks',
                'brief_description': 'Simple masks showing different emotions to help children identify and express feelings.',
                'steps_to_make': '''1. Cut face shapes from paper plates
2. Draw or paste pictures showing basic emotions: happy, sad, angry, surprised, scared
3. Attach craft sticks as handles
4. Create a feelings mirror for children to practice expressions
5. Include emotion picture books''',
                'tips_for_use': '''- Start with happy and sad, gradually add others
- Use masks during story time to show character emotions
- Encourage children to make faces behind masks
- Ask "How does this character feel?" during stories
- Use for conflict resolution: "Show me how you felt"''',
                'materials': ['Paper plates', 'Washable markers', 'Pipe cleaners', 'Mirrors'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'low',
                'learning_outcome': 'Children will identify basic emotions and express their own feelings appropriately.',
                'learning_styles': ['Visual Learner', 'Social Learner', 'Kinesthetic Learner'],
                'special_needs': ['Social Anxiety', 'Speech Delay', 'Autism Spectrum'],
                'themes': ['My Feelings', 'All About Me']
            }
        ]
        
        for tlr_data in tlrs:
            self.create_tlr(tlr_data, nursery, arts_subject)

    def create_environmental_studies_tlrs(self):
        nursery = ClassLevel.objects.get(name="Nursery")
        env_subject = Subject.objects.get(class_level=nursery, title="Environmental Studies")
        
        tlrs = [
            {
                'title': 'Weather Observation Chart',
                'brief_description': 'Interactive chart for daily weather observation and recording, developing scientific thinking.',
                'steps_to_make': '''1. Create large poster board with days of the week
2. Design weather symbol cards: sunny, cloudy, rainy, windy
3. Add pockets or velcro strips for moveable symbols
4. Include thermometer picture and simple temperature indicators
5. Create weather clothing matching cards''',
                'tips_for_use': '''- Use during morning circle time daily
- Look outside together and discuss observations
- Let children choose appropriate weather symbols
- Connect weather to clothing choices
- Keep simple weather journal with pictures''',
                'materials': ['Cardboard', 'Colored paper', 'Washable markers', 'Color wheels'],
                'time_needed': 'starter',
                'intended_use': 'aid',
                'tlr_type': 'poster',
                'class_size': 'large',
                'bloom_level': 'understand',
                'budget_band': 'low',
                'learning_outcome': 'Children will observe and describe daily weather patterns and make connections between weather and appropriate clothing.',
                'learning_styles': ['Visual Learner', 'Social Learner'],
                'special_needs': ['Attention Difficulties'],
                'themes': ['Weather and Seasons', 'My Environment']
            },
            {
                'title': 'Community Helper Role Play Kit',
                'brief_description': 'Dress-up items and props representing different community helpers to promote social awareness.',
                'steps_to_make': '''1. Gather simple costume pieces for each helper:
   - Doctor: white coat, stethoscope, medical bag
   - Firefighter: red hat, hose, badge
   - Teacher: books, glasses, pointer
   - Police officer: hat, badge, whistle
   - Chef: apron, hat, wooden spoons
2. Create matching picture cards showing each helper
3. Add props specific to each job''',
                'tips_for_use': '''- Introduce one helper at a time during dramatic play
- Ask children about helpers they know in their community
- Encourage role playing: "What does a doctor do?"
- Connect to field trips or community visits
- Use during discussions about safety and help''',
                'materials': ['Fabric scraps', 'Picture books', 'Dress-up items', 'Small containers'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify community helpers and describe how they help people in the community.',
                'learning_styles': ['Social Learner', 'Kinesthetic Learner'],
                'special_needs': ['Social Anxiety', 'Speech Delay'],
                'themes': ['Community Helpers', 'My Community']
            }
        ]
        
        for tlr_data in tlrs:
            self.create_tlr(tlr_data, nursery, env_subject)

    def create_physical_development_tlrs(self):
        nursery = ClassLevel.objects.get(name="Nursery")
        phys_subject = Subject.objects.get(class_level=nursery, title="Physical Development")
        
        tlrs = [
            {
                'title': 'Body Parts Learning Mirror',
                'brief_description': 'Unbreakable mirror with body part labels to promote self-awareness and vocabulary development.',
                'steps_to_make': '''1. Mount large unbreakable mirror at child height
2. Create removable labels for body parts (head, arms, legs, hands, feet, eyes, nose, mouth)
3. Use bright colors and simple pictures alongside words
4. Add velcro so children can move labels
5. Include "Simon Says" instruction cards''',
                'tips_for_use': '''- Start with major body parts, add details gradually
- Sing body part songs while looking in mirror
- Play "Touch your..." games
- Encourage children to point to parts on themselves and others
- Use during discussions about keeping our bodies healthy''',
                'materials': ['Mirrors', 'Colored paper', 'Washable markers', 'Picture cards'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'poster',
                'class_size': 'small',
                'bloom_level': 'remember',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify and name major body parts and develop body awareness.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Developmental Delays', 'Motor Delays'],
                'themes': ['My Body', 'All About Me']
            },
            {
                'title': 'Fine Motor Threading Cards',
                'brief_description': 'Large threading cards with simple patterns to develop hand-eye coordination and concentration.',
                'steps_to_make': '''1. Cut large shapes from cardboard (circle, square, heart, star)
2. Punch holes around the edges, about 2cm apart
3. Cover with clear contact paper for durability
4. Provide thick yarn or shoelaces with taped ends
5. Create pattern cards showing different threading designs''',
                'tips_for_use': '''- Demonstrate threading technique first
- Start with just a few holes, increase gradually
- Encourage children to create their own patterns
- Use during quiet time or as a calming activity
- Celebrate completed projects with enthusiasm''',
                'materials': ['Cardboard', 'Yarn', 'Safety scissors', 'Shape cutouts'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'low',
                'learning_outcome': 'Children will develop fine motor skills and hand-eye coordination through threading activities.',
                'learning_styles': ['Kinesthetic Learner', 'Solitary Learner'],
                'special_needs': ['Motor Delays', 'Attention Difficulties'],
                'themes': ['My School']
            }
        ]
        
        for tlr_data in tlrs:
            self.create_tlr(tlr_data, nursery, phys_subject)

    def create_music_movement_tlrs(self):
        nursery = ClassLevel.objects.get(name="Nursery")
        music_subject = Subject.objects.get(class_level=nursery, title="Music and Movement")
        
        tlrs = [
            {
                'title': 'Rhythm Instrument Collection',
                'brief_description': 'Simple homemade instruments for exploring rhythm, beat, and musical expression.',
                'steps_to_make': '''1. Create various instruments:
   - Shakers: plastic bottles with rice/beans
   - Drums: empty containers with tight lids
   - Bells: sew bells onto elastic bands
   - Rhythm sticks: decorated wooden dowels
   - Tambourines: paper plates with bottle caps attached
2. Decorate each instrument with colorful designs
3. Store in a music basket''',
                'tips_for_use': '''- Start with one instrument at a time
- Demonstrate how to hold and play each instrument
- Play music and encourage children to keep the beat
- Use instruments during singing time
- Create simple rhythm patterns for children to copy''',
                'materials': ['Plastic bottles', 'Bells', 'Paper plates', 'Bottle caps', 'Drums', 'Popsicle sticks'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'low',
                'learning_outcome': 'Children will explore rhythm and beat while developing gross motor coordination and musical expression.',
                'learning_styles': ['Auditory Learner', 'Kinesthetic Learner'],
                'special_needs': ['Sensory Processing', 'Speech Delay'],
                'themes': ['Festivals and Celebrations']
                },
            {
                'title': 'Movement Scarves and Dance Props',
                'brief_description': 'Colorful scarves and props for creative movement, following music, and expressing emotions through dance.',
                'steps_to_make': '''1. Gather lightweight scarves in different colors
2. Create simple dance props:
   - Ribbon wands with craft sticks
   - Jingle bell bracelets with elastic
   - Flowing streamers attached to rings
3. Prepare movement instruction cards with pictures
4. Set up open space for safe movement''',
                'tips_for_use': '''- Play different types of music (fast, slow, gentle, exciting)
- Demonstrate movements first, then let children explore
- Use scarves to show emotions: "Show me happy dancing!"
- Encourage free expression without "right" or "wrong" movements
- Include cultural music and traditional dances''',
                'materials': ['Scarves', 'Craft sticks', 'Bells', 'Ribbon', 'Elastic bands'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'large',
                'bloom_level': 'create',
                'budget_band': 'low',
                'learning_outcome': 'Children will express themselves through creative movement and develop gross motor skills while responding to different musical rhythms.',
                'learning_styles': ['Kinesthetic Learner', 'Auditory Learner'],
                'special_needs': ['Social Anxiety', 'Motor Delays'],
                'themes': ['Festivals and Celebrations', 'My Feelings']
            }
        ]
        
        for tlr_data in tlrs:
            self.create_tlr(tlr_data, nursery, music_subject)

    def create_additional_comprehensive_tlrs(self):
        """Create additional TLRs using the expanded materials list"""
        nursery = ClassLevel.objects.get(name="Nursery")
        
        # Cross-curricular TLRs
        additional_tlrs = [
            {
                'title': 'Ghanaian Culture Kente Pattern Cards',
                'brief_description': 'Interactive cards featuring traditional Kente patterns for cultural awareness and pattern recognition.',
                'subject': 'Creative Arts',
                'steps_to_make': '''1. Research authentic Kente patterns and their meanings
2. Create large pattern cards using colored EVA foam sheets
3. Cut out individual pattern pieces for children to recreate designs
4. Include story cards explaining the cultural significance
5. Add Kente fabric scraps for tactile exploration
6. Laminate cards for durability''',
                'tips_for_use': '''- Share simple stories about Kente cloth traditions
- Let children feel real Kente fabric pieces
- Start with simple patterns, progress to more complex
- Encourage children to create their own patterns
- Connect to discussions about Ghanaian heritage and pride''',
                'materials': ['Kente offcuts', 'EVA foam sheet', 'Glitter EVA foam sheet', 'Laminating pouches', 'Manila cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will recognize traditional Kente patterns and develop cultural pride while practicing pattern recognition skills.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Attention Difficulties'],
                'themes': ['My Community', 'Festivals and Celebrations']
            },
            {
                'title': 'Touch and Feel Letter Learning Bags',
                'brief_description': 'Sensory bags containing textured materials shaped like letters for tactile letter recognition.',
                'subject': 'Language and Literacy',
                'steps_to_make': '''1. Create letter shapes using different textured materials:
   - Sandpaper letters for rough texture
   - Cotton wool letters for soft texture
   - Foil paper letters for smooth texture
   - Beans glued in letter shapes for bumpy texture
2. Store each letter in individual Ziploc bags
3. Include corresponding picture cards
4. Add instruction cards for activities''',
                'tips_for_use': '''- Let children trace letters with their finger while saying the sound
- Play "mystery letter" games with eyes closed
- Connect letters to children\'s names and familiar words
- Use during quiet time for individual exploration
- Encourage children to describe how each letter feels''',
                'materials': ['Ziploc bags', 'Cotton wool', 'Foil paper', 'Beans', 'Double sided tape', 'Manila cards'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'remember',
                'budget_band': 'low',
                'learning_outcome': 'Children will recognize letters through multi-sensory exploration and begin to associate letters with their sounds.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Visual Impairment', 'Sensory Processing', 'Attention Difficulties'],
                'themes': ['All About Me']
            },
            {
                'title': 'Water Transfer and Measurement Station',
                'brief_description': 'Hands-on water play station for developing pre-math concepts and fine motor skills.',
                'subject': 'Numeracy',
                'steps_to_make': '''1. Set up water table or large plastic container
2. Provide various sized containers: small cups, large bowls, squeeze bottles
3. Add measuring tools: plastic spoons, small pitchers, funnels
4. Include floating and sinking objects for experimentation
5. Create waterproof instruction cards with pictures
6. Provide towels and aprons for easy cleanup''',
                'tips_for_use': '''- Demonstrate careful pouring techniques
- Use language: "full", "empty", "more", "less", "same"
- Count while pouring: "1 cup, 2 cups, 3 cups"
- Ask prediction questions: "Which holds more water?"
- Allow free exploration and discovery''',
                'materials': ['Small plastic containers', 'Plastic spoons', 'Water', 'Transparent sheets', 'Sponge pieces'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'none',
                'learning_outcome': 'Children will explore measurement concepts, develop hand-eye coordination, and understand volume relationships.',
                'learning_styles': ['Kinesthetic Learner', 'Nature Learner'],
                'special_needs': ['Motor Delays', 'Attention Difficulties'],
                'themes': ['My Environment']
            },
            {
                'title': 'Family Photo Memory Matching Game',
                'brief_description': 'Personalized matching game using children\'s family photos to promote social-emotional development.',
                'subject': 'Environmental Studies',
                'steps_to_make': '''1. Request family photos from parents (2 copies of each)
2. Mount photos on sturdy cardboard backing
3. Cover with clear contact paper for protection
4. Create family vocabulary cards (mama, papa, baby, etc.)
5. Add simple family tree templates
6. Store in decorated container''',
                'tips_for_use': '''- Start with each child\'s own family photos
- Encourage children to talk about their families
- Play simple matching games with 4-6 photo pairs
- Use during discussions about different family structures
- Respect and celebrate all types of families''',
                'materials': ['Printed images', 'Cardboard boxes', 'Clear contact paper', 'Manila cards', 'Markers'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'game',
                'class_size': 'small',
                'bloom_level': 'understand',
                'budget_band': 'low',
                'learning_outcome': 'Children will develop memory skills, practice turn-taking, and express pride in their family relationships.',
                'learning_styles': ['Visual Learner', 'Social Learner'],
                'special_needs': ['Social Anxiety', 'Speech Delay'],
                'themes': ['My Family', 'All About Me']
            },
            {
                'title': 'Balance and Coordination Obstacle Course',
                'brief_description': 'Indoor obstacle course using safe materials to develop gross motor skills and body awareness.',
                'subject': 'Physical Development',
                'steps_to_make': '''1. Design course with different stations:
   - Masking tape lines for walking balance
   - Hula hoops for stepping through
   - Bean bags for tossing into containers
   - Tunnel made from large cardboard box
   - Balance beam from wide wooden plank
2. Create instruction picture cards for each station
3. Ensure all materials are safe and age-appropriate''',
                'tips_for_use': '''- Demonstrate each station before children begin
- Encourage effort rather than speed or perfection
- Allow children to repeat favorite stations
- Modify difficulty based on individual abilities
- Use encouraging language and celebrate attempts''',
                'materials': ['Masking tape', 'Hula hoops', 'Bean bags', 'Cardboard boxes', 'Picture cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'game',
                'class_size': 'medium',
                'bloom_level': 'apply',
                'budget_band': 'low',
                'learning_outcome': 'Children will develop gross motor skills, body coordination, and confidence in physical movement.',
                'learning_styles': ['Kinesthetic Learner'],
                'special_needs': ['Motor Delays', 'Attention Difficulties'],
                'themes': ['My Body']
            },
            {
                'title': 'Sound Discovery Bottles',
                'brief_description': 'Clear bottles filled with different materials to create various sounds for auditory discrimination.',
                'subject': 'Music and Movement',
                'steps_to_make': '''1. Use clear plastic bottles of the same size
2. Fill each bottle with different materials:
   - Rice for soft shaking sound
   - Beans for medium rattling
   - Bottle caps for loud clanking
   - Bells for jingling
   - Beads for rolling sound
3. Secure lids tightly with glue
4. Create matching sound cards with pictures''',
                'tips_for_use': '''- Let children explore sounds freely first
- Play "guess the sound" games with eyes closed
- Use bottles to accompany songs and rhymes
- Encourage children to describe sounds: loud, soft, fast, slow
- Create simple rhythm patterns with different bottles''',
                'materials': ['Plastic bottles', 'Rice', 'Beans', 'Bottle caps', 'Bells', 'Beads', 'Paper glue'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'analyze',
                'budget_band': 'low',
                'learning_outcome': 'Children will develop auditory discrimination skills and explore cause-and-effect relationships through sound.',
                'learning_styles': ['Auditory Learner', 'Kinesthetic Learner'],
                'special_needs': ['Hearing Impairment', 'Sensory Processing'],
                'themes': ['My Environment']
            }
        ]
        
        # Create these additional TLRs
        for tlr_data in additional_tlrs:
            subject = Subject.objects.get(class_level=nursery, title=tlr_data['subject'])
            self.create_tlr(tlr_data, nursery, subject)

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