# management/commands/create_interactive_tlrs.py
from django.core.management.base import BaseCommand
from suggestor.models import (
    ClassLevel, Subject, Theme, KeyLearningArea, CoreCompetency, 
    GoalTag, ResourceType, SpecialNeed, LearningStyle, Material, Tlr
)

class Command(BaseCommand):
    help = 'Create interactive, hands-on DIY TLRs for nursery level'

    def handle(self, *args, **options):
        self.stdout.write('Creating interactive hands-on TLRs...')
        
        nursery = ClassLevel.objects.get(name="Nursery")
        
        # Create interactive TLRs for each subject
        self.create_interactive_language_tlrs(nursery)
        self.create_interactive_numeracy_tlrs(nursery)
        self.create_interactive_social_emotional_tlrs(nursery)
        self.create_interactive_environmental_tlrs(nursery)
        self.create_interactive_creative_tlrs(nursery)
        self.create_additional_subject_tlrs(nursery)
        self.create_cross_curricular_interactive_tlrs(nursery)
        
        self.stdout.write(self.style.SUCCESS('Interactive TLRs created successfully!'))

    def create_interactive_language_tlrs(self, nursery):
        lang_subject = Subject.objects.get(class_level=nursery, title="Language and Literacy")
        
        interactive_lang_tlrs = [
            {
                'title': 'Interactive Sentence Formation Slider',
                'brief_description': 'Sliding word strips that children can move to form simple sentences with picture cues.',
                'steps_to_make': '''1. Create a large cardboard base (50cm x 30cm) with three horizontal slots
2. Cut sliding strips from manila cards for:
   - Strip 1 (WHO): Pictures + words - boy, girl, cat, dog, mama, papa
   - Strip 2 (ACTION): Pictures + words - runs, jumps, eats, sleeps, plays, sits
   - Strip 3 (WHERE/WHAT): Pictures + words - home, school, ball, food, bed, garden
3. Laminate all pieces for durability
4. Thread colorful ribbon through slots to guide sliding motion
5. Add velcro dots at end positions to hold strips in place
6. Decorate with bright colors and fun characters''',
                'tips_for_use': '''- Start with simple combinations: "Boy runs home"
- Let children slide strips and read the sentence together
- Encourage silly combinations for fun: "Cat eats school"
- Use pictures as primary cues, words as secondary
- Ask "What happens when we change this word?"
- Create actions for sentences: act out "boy jumps"''',
                'materials': ['Cardboard boxes', 'Manila cards', 'Laminating pouches', 'Ribbon', 'Velcro dots', 'Markers', 'Printed images'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will understand sentence structure and create simple sentences by manipulating word and picture combinations.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Speech Delay', 'Attention Difficulties'],
                'themes': ['My School', 'My Family']
            },
            {
                'title': 'Interactive Three-Letter Word Building Slider',
                'brief_description': 'Rotating wheels and sliding cards that help children build and blend three-letter words.',
                'steps_to_make': '''1. Create three circular wheels from thick cardboard:
   - Wheel 1: Beginning sounds (b, c, d, f, h, m, p, r, s, t)
   - Wheel 2: Middle vowels (a, e, i, o, u) in bright colors
   - Wheel 3: Ending sounds (t, n, g, p, d, m, s, x)
2. Cut window spaces in base board to show one letter from each wheel
3. Use brass fasteners to attach rotating wheels
4. Add corresponding picture cards that slide into pockets below
5. Include simple three-letter words: cat, dog, pig, sun, bag, etc.
6. Color-code vowels differently from consonants''',
                'tips_for_use': '''- Demonstrate turning wheels to form real words first
- Start with familiar words: cat, dog, run, big
- Sound out each letter as wheels turn: "c-a-t makes cat!"
- Let children experiment with nonsense words too
- Match picture cards to words they create
- Use in pairs for collaborative learning''',
                'materials': ['Cardboard boxes', 'Brass fasteners', 'Manila cards', 'EVA foam sheet', 'Markers', 'Velcro strips', 'Picture cards'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will blend letter sounds to form three-letter words and understand basic phonetic principles.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Speech Delay', 'Attention Difficulties'],
                'themes': ['All About Me']
            },
            {
                'title': 'Jolly Phonics Interactive Sound Garden',
                'brief_description': 'Three-dimensional garden scene with moveable characters and objects for each phonics sound.',
                'steps_to_make': '''1. Create garden base from large cardboard box lid (painted green)
2. Make 3D elements for each Jolly Phonics sound:
   - 's' snake that winds through garden (green pipe cleaner)
   - 'a' ants marching (black pom-poms with legs)
   - 't' tiger behind trees (orange felt with stripes)
   - 'i' inchworm (green sections that bend)
   - 'p' pig in pen (pink felt with moveable parts)
   - 'n' net for catching (actual small net)
3. Add interactive elements: flip trees, opening flowers, moving gates
4. Include action cards showing Jolly Phonics gestures
5. Create pockets for letter cards throughout garden''',
                'tips_for_use': '''- Introduce one sound per session using the garden story
- Encourage children to move objects while making sounds
- Practice Jolly Phonics actions with garden characters
- Hide letters in garden for treasure hunts
- Let children create their own garden stories
- Use for sound recognition games: "Find something that starts with 's'"''',
                'materials': ['Cardboard boxes', 'Pipe cleaners', 'Felt pieces', 'Pom-poms', 'EVA foam sheet', 'Velcro dots', 'Small containers'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'remember',
                'budget_band': 'medium',
                'learning_outcome': 'Children will recognize letter sounds through multi-sensory exploration and associate sounds with actions and objects.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner', 'Social Learner'],
                'special_needs': ['Speech Delay', 'Sensory Processing'],
                'themes': ['Plants and Nature', 'Animals Around Me']
            },
            {
                'title': 'Vowels Activity Mat with Pop-Up Letters',
                'brief_description': 'Interactive floor mat where children step on pictures to reveal pop-up vowel letters with sounds.',
                'steps_to_make': '''1. Create large mat from canvas or thick fabric (1m x 1m)
2. Sew or attach 15 pockets in grid pattern
3. For each vowel, create 3 picture cards that pop up:
   - A: apple, ant, alligator
   - E: elephant, egg, envelope  
   - I: igloo, insect, ice cream
   - O: octopus, orange, owl
   - U: umbrella, up arrow, unicorn
4. Add spring mechanism using cardboard and elastic for pop-up effect
5. Record vowel sounds on simple sound buttons (or use voice)
6. Include instruction cards with movements''',
                'tips_for_use': '''- Children step on pictures to make vowels pop up
- Say vowel sound each time it pops up
- Play vowel hunt: "Step on things that start with 'a'"
- Use for group activities and turn-taking
- Encourage children to make vowel mouth shapes
- Add music and dance to vowel stepping''',
                'materials': ['Scrap fabric', 'EVA foam sheet', 'Elastic bands', 'Velcro dots', 'Picture cards', 'Sound buttons'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'game',
                'class_size': 'medium',
                'bloom_level': 'remember',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify vowel sounds and associate them with corresponding pictures through active movement.',
                'learning_styles': ['Kinesthetic Learner', 'Auditory Learner'],
                'special_needs': ['Motor Delays', 'Attention Difficulties'],
                'themes': ['My Body', 'Animals Around Me']
            },
            {
                'title': 'Letter Sounds Spinning Wheel Chart',
                'brief_description': 'Large spinning wheel with letter sounds that children rotate to match pictures and practice pronunciation.',
                'steps_to_make': '''1. Create large circular base (60cm diameter) from cardboard
2. Design rotating top wheel with 26 letter sections
3. Cut window in base to reveal one letter at a time
4. Around base, attach 26 picture pockets with velcro
5. Include multiple picture cards for each letter sound
6. Add arrow pointer and decorative elements
7. Use different textures for each letter (sandpaper, felt, smooth)
8. Include mirror for children to watch mouth movements''',
                'tips_for_use': '''- Spin wheel and say letter sound together
- Find picture cards that match the letter sound
- Look in mirror while making sounds
- Feel textured letters while saying sounds
- Play in pairs: one spins, other finds pictures
- Use for assessment: "Show me the letter that makes 'mmmm'"''',
                'materials': ['Cardboard boxes', 'Brass fasteners', 'Velcro strips', 'Picture cards', 'Textured papers', 'Small mirrors', 'Markers'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'poster',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will recognize all letter sounds and match them to appropriate pictures while developing phonemic awareness.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner', 'Auditory Learner'],
                'special_needs': ['Speech Delay', 'Hearing Impairment'],
                'themes': ['My School']
            }
        ]
        
        for tlr_data in interactive_lang_tlrs:
            self.create_tlr(tlr_data, nursery, lang_subject)

    def create_interactive_numeracy_tlrs(self, nursery):
        num_subject = Subject.objects.get(class_level=nursery, title="Numeracy")
        
        interactive_num_tlrs = [
            {
                'title': 'Interactive Shapes Discovery Box',
                'brief_description': 'Multi-compartment box with shape sorters, puzzles, and real-world shape matching activities.',
                'steps_to_make': '''1. Use large cardboard box, divide into 6 compartments
2. Cut shape holes in top (circle, square, triangle, rectangle, oval, diamond)
3. Create shape puzzle pieces from different materials:
   - Wooden circles, cardboard squares, felt triangles
   - Textured rectangles, smooth ovals, glittery diamonds
4. Add shape sorting tubes for each shape
5. Include real objects collection for each shape
6. Create flip cards showing shapes in environment
7. Add shape stamps and ink pads for printing''',
                'tips_for_use': '''- Start with basic shapes, add complex ones gradually
- Let children feel shapes before looking
- Practice shape names in English and local language
- Go on shape hunts around classroom
- Use shapes to create pictures and patterns
- Sort objects by shape, then by color, then by size''',
                'materials': ['Cardboard boxes', 'EVA foam sheet', 'Felt pieces', 'Wooden blocks', 'Shape cutouts', 'Ink pads', 'Real objects'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'analyze',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify, sort, and compare geometric shapes while connecting them to real-world objects.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Visual Impairment', 'Motor Delays'],
                'themes': ['My Environment', 'My School']
            },
            {
                'title': 'Color Mixing Magic Wheel',
                'brief_description': 'Rotating color wheels that show primary color combinations creating secondary colors with surprise reveals.',
                'steps_to_make': '''1. Create three transparent wheels from clear plastic sheets
2. Paint primary colors (red, blue, yellow) on separate wheels
3. Design overlapping mechanism showing color mixing
4. Add rotating handle for children to control
5. Include color surprise windows that reveal mixed colors
6. Create color matching game cards
7. Add real objects in primary and secondary colors
8. Include color mixing bottles with safe materials''',
                'tips_for_use': '''- Demonstrate primary colors first
- Let children predict what happens when colors mix
- Use surprise reveals: "What color will we make?"
- Connect to nature: "What color is grass? Sky? Sun?"
- Practice color names in different languages
- Use for art projects: mix real paints safely''',
                'materials': ['Transparent sheets', 'Colored paints', 'Brass fasteners', 'Clear bottles', 'Safe mixing materials', 'Real colored objects'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'small',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify primary and secondary colors and understand how colors combine to create new colors.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Visual Impairment', 'Attention Difficulties'],
                'themes': ['My Environment', 'Creative Arts']
            }
        ]
        
        for tlr_data in interactive_num_tlrs:
            self.create_tlr(tlr_data, nursery, num_subject)

    def create_interactive_social_emotional_tlrs(self, nursery):
        creative_subject = Subject.objects.get(class_level=nursery, title="Creative Arts")
        
        interactive_social_tlrs = [
            {
                'title': 'Good Manners Garden Interactive Scene',
                'brief_description': 'Three-dimensional garden scene where children move characters to practice polite behaviors and social skills.',
                'steps_to_make': '''1. Create garden base from large box lid with green fabric landscape
2. Design moveable character dolls (diverse children, adults, animals)
3. Create scenario stations around garden:
   - Sharing station: playground with swings and toys
   - Helping station: fallen items that need picking up  
   - Greeting station: house with doorway for visitors
   - Thank you station: gift exchange area
   - Sorry station: conflict resolution space
4. Include speech bubble cards with polite phrases
5. Add props: toys to share, gifts to exchange, cleaning tools
6. Create situation cards for role-playing''',
                'tips_for_use': '''- Model good manners using garden characters first
- Let children move dolls through different scenarios
- Practice phrases: "Please", "Thank you", "Sorry", "Excuse me"
- Encourage children to create their own polite situations
- Connect to real classroom situations
- Use during conflict resolution times''',
                'materials': ['Cardboard boxes', 'Fabric scraps', 'Small dolls', 'Felt pieces', 'Speech bubbles', 'Small props', 'Manila cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will practice polite behaviors and social skills through interactive role-playing scenarios.',
                'learning_styles': ['Social Learner', 'Kinesthetic Learner'],
                'special_needs': ['Social Anxiety', 'Speech Delay'],
                'themes': ['My Community', 'My School']
            },
            {
                'title': 'Emotions Flip and Match Interactive Chart',
                'brief_description': 'Multi-layered chart with flip panels showing different emotions, causes, and appropriate responses.',
                'steps_to_make': '''1. Create large base chart (70cm x 50cm) with emotion categories
2. Design flip panels for each emotion:
   - Happy: smiley face flips to show causes (friends, treats, success)
   - Sad: sad face flips to show causes (injury, loss, disappointment)
   - Angry: angry face flips to show causes (frustration, unfairness)
   - Scared: worried face flips to show causes (loud noises, darkness)
   - Excited: enthusiastic face flips to show causes (parties, surprises)
3. Add response panels showing appropriate actions for each emotion
4. Include emotion mirror for children to practice expressions
5. Create emotion matching games with situation cards''',
                'tips_for_use': '''- Start with basic happy/sad emotions
- Let children flip panels to explore emotions
- Practice making faces in the emotion mirror
- Discuss: "When do you feel this way?"
- Use during daily check-ins: "How are you feeling today?"
- Connect emotions to stories and real situations''',
                'materials': ['Manila cards', 'Mirrors', 'Velcro strips', 'Markers', 'Laminating pouches', 'Picture cards'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'poster',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify different emotions, understand their causes, and learn appropriate responses to feelings.',
                'learning_styles': ['Visual Learner', 'Social Learner'],
                'special_needs': ['Social Anxiety', 'Autism Spectrum'],
                'themes': ['My Feelings', 'All About Me']
            }
        ]
        
        for tlr_data in interactive_social_tlrs:
            self.create_tlr(tlr_data, nursery, creative_subject)

    def create_interactive_environmental_tlrs(self, nursery):
        env_subject = Subject.objects.get(class_level=nursery, title="Environmental Studies")
        
        interactive_env_tlrs = [
            {
                'title': 'My Weather Station Interactive Chart',
                'brief_description': 'Dynamic weather station with moveable elements, temperature gauge, and daily weather tracking system.',
                'steps_to_make': '''1. Create weather station base from large cardboard (80cm x 60cm)
2. Design moveable weather elements:
   - Sliding sun that moves across sky track
   - Cloud shapes that attach with velcro for cloudy days
   - Rain drops that hang from clouds with blue ribbon
   - Wind spinner made from pinwheel
   - Temperature gauge with moving arrow
3. Add weather clothing dress-up doll with seasonal outfits
4. Include weather prediction cards and daily tracking chart
5. Create weather sounds (rain stick, wind chimes, thunder drum)''',
                'tips_for_use': '''- Check weather together each morning
- Let children move weather elements to match outside
- Dress weather doll appropriately for conditions
- Make weather sounds while updating chart
- Predict tomorrow's weather together
- Connect weather to activities: "Good day for outdoor play?"''',
                'materials': ['Cardboard boxes', 'Velcro strips', 'Ribbon', 'Pinwheels', 'Moveable arrow', 'Weather sounds', 'Dress-up clothes'],
                'time_needed': 'starter',
                'intended_use': 'aid',
                'tlr_type': 'poster',
                'class_size': 'large',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will observe, record, and predict weather patterns while connecting weather to appropriate clothing and activities.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Attention Difficulties'],
                'themes': ['Weather and Seasons', 'My Environment']
            },
            {
                'title': 'Food Groups Sorting Kitchen',
                'brief_description': 'Interactive play kitchen with sorting stations for different food groups and healthy eating activities.',
                'steps_to_make': '''1. Convert large cardboard box into play kitchen with compartments
2. Create food group sorting stations:
   - Fruits basket with realistic fruit models
   - Vegetable garden box with root vegetables
   - Protein station with fish, chicken, beans models
   - Grains basket with rice, bread, corn models
   - Dairy refrigerator section with milk, cheese models
3. Add interactive elements: opening refrigerator, turning stove knobs
4. Include shopping lists and meal planning cards
5. Create "healthy plate" template for balanced meals
6. Add cooking utensils and play food preparation tools''',
                'tips_for_use': '''- Sort foods into correct groups together
- Plan balanced meals using healthy plate template
- Role-play shopping and cooking scenarios
- Discuss where foods come from: "Apples grow on trees"
- Practice food names in English and local languages
- Connect to family meals and cultural foods''',
                'materials': ['Cardboard boxes', 'Play food models', 'Small containers', 'Cooking utensils', 'Manila cards', 'Velcro strips'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'analyze',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify different food groups and understand the importance of balanced, healthy eating.',
                'learning_styles': ['Kinesthetic Learner', 'Social Learner'],
                'special_needs': ['Developmental Delays'],
                'themes': ['Food and Nutrition', 'My Home']
            },
            {
                'title': 'Fruits and Vegetables Growing Garden',
                'brief_description': 'Interactive garden scene showing how fruits and vegetables grow with removeable parts and growth stages.',
                'steps_to_make': '''1. Create garden landscape from green fabric on large base
2. Design growing plants with removeable parts:
   - Carrot tops that pull out to reveal orange carrots below
   - Apple tree with velcro apples that can be "picked"
   - Tomato plant with different colored tomatoes (green to red)
   - Bean plants with pods that open to show beans inside
   - Corn stalks with husks that peel back
3. Add garden tools: watering can, hoe, basket for harvesting
4. Include seed packets matching each plant
5. Create growth sequence cards showing plant development''',
                'tips_for_use': '''- Plant seeds and watch simulated growth process
- Harvest fruits and vegetables when "ready"
- Sort by where they grow: underground, on trees, on vines
- Practice healthy eating discussions
- Connect to real gardening if possible
- Use for counting activities: "How many apples?"''',
                'materials': ['Fabric scraps', 'Velcro strips', 'Garden tools', 'Seed packets', 'Growth cards', 'Harvest baskets'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will understand how fruits and vegetables grow and develop appreciation for healthy foods.',
                'learning_styles': ['Kinesthetic Learner', 'Nature Learner'],
                'special_needs': ['Attention Difficulties'],
                'themes': ['Plants and Nature', 'Food and Nutrition']
            },
            {
                'title': 'Transportation Interactive Journey Board',
                'brief_description': 'Large board game-style mat with moveable vehicles and journey scenarios for exploring different means of transport.',
                'steps_to_make': '''1. Create large mat (1.5m x 1m) showing different travel routes:
   - Road with traffic lights and signs
   - Railway track with stations
   - River with bridges
   - Airport runway
   - Sea with ports
2. Design moveable vehicles for each route:
   - Cars, buses, motorcycles for roads
   - Trains for railway
   - Boats for water
   - Airplanes for sky
3. Add interactive elements: working traffic lights, opening bridges
4. Include journey cards showing different trips
5. Create sound effects for each vehicle type''',
                'tips_for_use': '''- Move vehicles along appropriate routes
- Practice vehicle sounds and names
- Discuss when to use different transportation
- Plan imaginary journeys: "How do we get to Kumasi?"
- Practice road safety rules
- Connect to children\'s real travel experiences''',
                'materials': ['Large fabric mat', 'Toy vehicles', 'Traffic signs', 'Sound makers', 'Journey cards', 'Interactive elements'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'game',
                'class_size': 'medium',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify different means of transportation and understand appropriate uses for various vehicles.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Attention Difficulties', 'Motor Delays'],
                'themes': ['Transportation', 'My Community']
            }
        ]
        
        for tlr_data in interactive_env_tlrs:
            self.create_tlr(tlr_data, nursery, env_subject)

    def create_interactive_creative_tlrs(self, nursery):
        creative_subject = Subject.objects.get(class_level=nursery, title="Creative Arts")
        
        interactive_creative_tlrs = [
            {
                'title': 'Musical Pattern Stepping Mat',
                'brief_description': 'Large floor mat with different textures and sounds that children step on to create musical patterns and rhythms.',
                'steps_to_make': '''1. Create large mat base (2m x 1m) from durable fabric
2. Attach different textured sections:
   - Bubble wrap squares for "pop" sounds
   - Crinkly material patches for "crunch" sounds  
   - Bell strips sewn in for "jingle" sounds
   - Velcro patches for "scratch" sounds
   - Smooth satin for "swoosh" sounds
3. Color-code each texture with bright colors
4. Add pattern instruction cards showing step sequences
5. Include rhythm sticks for children to tap along
6. Create removeable number markers (1-8) for sequence learning''',
                'tips_for_use': '''- Start with simple 2-3 step patterns
- Let children explore sounds freely first
- Create group activities: follow the leader
- Record children's favorite patterns to repeat
- Use for counting: "Step 4 times on the jingle squares"
- Encourage creative pattern making''',
                'materials': ['Large fabric pieces', 'Bubble wrap', 'Bells', 'Velcro strips', 'Satin fabric', 'Number markers', 'Rhythm sticks'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'game',
                'class_size': 'large',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will create and follow musical patterns while developing gross motor skills and rhythm awareness.',
                'learning_styles': ['Kinesthetic Learner', 'Auditory Learner'],
                'special_needs': ['Motor Delays', 'Sensory Processing'],
                'themes': ['Music and Movement', 'My Body']
            },
            {
                'title': 'Interactive Story Building Theater',
                'brief_description': 'Puppet theater with interchangeable backgrounds and moveable characters for collaborative storytelling.',
                'steps_to_make': '''1. Build theater frame from large cardboard box with cut-out stage opening
2. Create sliding background system:
   - Forest scene with moveable trees
   - Home scene with opening doors and windows
   - School scene with playground equipment
   - Market scene with stalls and vendors
3. Design finger puppets and stick puppets representing:
   - Family members, animals, community helpers
   - Emotions faces that attach to any character
4. Add interactive stage elements:
   - Spinning wheel for weather changes
   - Flip panels for day/night transitions
   - Sound effect buttons hidden behind stage
5. Include story starter cards and prop box''',
                'tips_for_use': '''- Let children choose characters and settings
- Start stories together: "Once upon a time..."
- Encourage children to take turns adding to stories
- Use for retelling familiar tales with new twists
- Practice problem-solving through story conflicts
- Record favorite stories to tell again''',
                'materials': ['Cardboard boxes', 'Finger puppets', 'Sliding backgrounds', 'Sound buttons', 'Story cards', 'Manila cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will develop narrative skills, creativity, and collaborative storytelling through interactive puppet theater.',
                'learning_styles': ['Visual Learner', 'Social Learner', 'Kinesthetic Learner'],
                'special_needs': ['Speech Delay', 'Social Anxiety'],
                'themes': ['My Family', 'Community Helpers', 'Festivals and Celebrations']
            }
        ]
        
        for tlr_data in interactive_creative_tlrs:
            self.create_tlr(tlr_data, nursery, creative_subject)

    def create_additional_subject_tlrs(self, nursery):
        """Create more subject-specific interactive TLRs"""
        
        # Physical Development TLRs
        phys_subject = Subject.objects.get(class_level=nursery, title="Physical Development")
        
        physical_tlrs = [
            {
                'title': 'Body Parts Interactive Mirror Game',
                'brief_description': 'Large mirror system with moveable body part labels and action command wheels for body awareness activities.',
                'steps_to_make': '''1. Mount large unbreakable mirror (60cm x 80cm) at child height
2. Create rotating command wheels around mirror edges:
   - Body parts wheel (head, arms, legs, hands, feet)
   - Action wheel (touch, wiggle, stretch, clap, stomp)
   - Number wheel (1, 2, 3, 4, 5)
3. Add velcro body part labels that stick to mirror
4. Include silly action cards: "Touch your nose 3 times"
5. Create body outline template that fits over mirror
6. Add costume box nearby for dress-up integration''',
                'tips_for_use': '''- Spin wheels to create action combinations
- Practice body part names while touching mirror image
- Play Simon Says using the command wheels
- Encourage silly combinations for laughter
- Use for emotional recognition: "Show me happy eyes"
- Connect to health discussions about body care''',
                'materials': ['Large mirrors', 'Rotating wheels', 'Velcro strips', 'Body part labels', 'Action cards', 'Dress-up items'],
                'time_needed': 'short',
                'intended_use': 'aid',
                'tlr_type': 'game',
                'class_size': 'small',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will identify body parts, follow multi-step instructions, and develop body awareness through interactive mirror play.',
                'learning_styles': ['Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Motor Delays', 'Developmental Delays'],
                'themes': ['My Body', 'All About Me']
            },
            {
                'title': 'Balance Challenge Adventure Course',
                'brief_description': 'Modular balance course with adjustable difficulty levels and interactive challenge cards.',
                'steps_to_make': '''1. Create balance beam sections from different materials:
   - Wide wooden plank (beginner level)
   - Rope laid on ground (intermediate)  
   - Narrow beam raised slightly (advanced)
2. Add textural walking surfaces:
   - Bubble wrap path for sensory input
   - Fabric patches with different textures
   - Number stepping stones in sequence
3. Include challenge station cards:
   - Walk while carrying object
   - Walk backwards
   - Stop and balance on one foot
   - Walk while clapping
4. Create adjustable height system using blocks
5. Add safety mats and colorful markings''',
                'tips_for_use': '''- Start with easiest level for all children
- Provide hand support initially, gradually reduce
- Celebrate every attempt, not just completion
- Create group cheering and encouragement
- Use for turn-taking and patience practice
- Adjust challenges based on individual abilities''',
                'materials': ['Wooden planks', 'Rope', 'Balance blocks', 'Texture materials', 'Challenge cards', 'Safety mats'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'game',
                'class_size': 'medium',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will develop balance, coordination, and confidence in physical movement while learning to assess and take appropriate risks.',
                'learning_styles': ['Kinesthetic Learner'],
                'special_needs': ['Motor Delays', 'Attention Difficulties'],
                'themes': ['My Body', 'Physical Development']
            }
        ]
        
        for tlr_data in physical_tlrs:
            self.create_tlr(tlr_data, nursery, phys_subject)
            
        # Music and Movement TLRs
        music_subject = Subject.objects.get(class_level=nursery, title="Music and Movement")
        
        music_tlrs = [
            {
                'title': 'Rhythm and Beat Building Station',
                'brief_description': 'Interactive station where children create, record, and replay rhythm patterns using various instruments and visual cues.',
                'steps_to_make': '''1. Set up rhythm station with instrument collection:
   - Homemade drums from various containers
   - Shakers with different fill materials
   - Rhythm sticks and clappers
   - Bell bracelets and anklets
2. Create visual rhythm cards using symbols:
   - Large dots for drums, wavy lines for shakers
   - Hand symbols for claps, foot symbols for stamps
3. Add recording system (simple voice recorder)
4. Include rhythm pattern templates with moveable pieces
5. Create conducting batons and simple sheet music
6. Set up performance stage area with microphone''',
                'tips_for_use': '''- Start with simple clap-clap-pause patterns
- Let children create their own rhythm cards
- Record patterns to play back and dance to
- Encourage conducting and leading others
- Connect rhythms to familiar songs
- Use for group cooperation and turn-taking''',
                'materials': ['Various containers', 'Rhythm instruments', 'Visual cards', 'Recording device', 'Conducting batons', 'Microphone'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'medium',
                'bloom_level': 'create',
                'budget_band': 'medium',
                'learning_outcome': 'Children will create and follow rhythm patterns while developing musical awareness and leadership skills.',
                'learning_styles': ['Auditory Learner', 'Kinesthetic Learner'],
                'special_needs': ['Speech Delay', 'Sensory Processing'],
                'themes': ['Music and Movement', 'Festivals and Celebrations']
            }
        ]
        
        for tlr_data in music_tlrs:
            self.create_tlr(tlr_data, nursery, music_subject)

    def create_cross_curricular_interactive_tlrs(self, nursery):
        """Create TLRs that span multiple subjects"""
        
        # These can be assigned to Language and Literacy but incorporate multiple subjects
        lang_subject = Subject.objects.get(class_level=nursery, title="Language and Literacy")
        
        cross_curricular_tlrs = [
            {
                'title': 'Community Helper Role-Play Communication Center',
                'brief_description': 'Interactive role-play center with communication tools, uniforms, and scenario cards for developing language through dramatic play.',
                'steps_to_make': '''1. Set up role-play stations for different community helpers:
   - Doctor station: white coat, stethoscope, patient charts
   - Teacher station: books, pointer, mini blackboard
   - Shop keeper station: cash register, play money, goods
   - Police station: hat, badge, radio, traffic signs
2. Create communication tools for each role:
   - Telephone for emergency calls
   - Prescription pads for doctors
   - Receipt books for shop keepers
   - Notebooks for teachers
3. Add scenario cards with problems to solve
4. Include community map showing where helpers work
5. Create simple uniforms and identification badges''',
                'tips_for_use': '''- Rotate children through different helper roles
- Encourage problem-solving conversations
- Practice polite communication phrases
- Connect to real community members children know
- Use for vocabulary building in context
- Practice asking for help appropriately''',
                'materials': ['Professional props', 'Communication tools', 'Scenario cards', 'Community map', 'Simple uniforms', 'Role-play materials'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'manipulative',
                'class_size': 'large',
                'bloom_level': 'apply',
                'budget_band': 'medium',
                'learning_outcome': 'Children will develop communication skills, vocabulary, and understanding of community roles through interactive dramatic play.',
                'learning_styles': ['Social Learner', 'Kinesthetic Learner', 'Visual Learner'],
                'special_needs': ['Speech Delay', 'Social Anxiety'],
                'themes': ['Community Helpers', 'My Community', 'Safety']
            },
            {
                'title': 'Seasonal Changes Discovery Wheel',
                'brief_description': 'Large rotating wheel showing seasonal changes with interactive elements that children can manipulate to explore weather, clothing, activities, and nature changes.',
                'steps_to_make': '''1. Create large circular base (80cm diameter) divided into 4 seasons
2. Design rotating overlay wheel with viewing windows
3. For each season section, include interactive elements:
   - Weather slider showing temperature and conditions
   - Clothing dress-up doll with seasonal outfits
   - Activity cards that flip to show seasonal games
   - Nature changes: tree with removeable leaves, flowers
4. Add month markers and special celebration indicators
5. Include seasonal food examples and cultural celebrations
6. Create prediction cards: "What comes next?"''',
                'tips_for_use': '''- Rotate wheel to current season and discuss
- Change doll's clothing to match weather
- Practice seasonal vocabulary and activities
- Predict upcoming changes: "What happens to leaves?"
- Connect to children's experiences: "What do you wear when it rains?"
- Use for calendar and time concepts''',
                'materials': ['Large circular base', 'Rotating mechanisms', 'Seasonal props', 'Dress-up doll', 'Weather indicators', 'Cultural celebration cards'],
                'time_needed': 'core',
                'intended_use': 'aid',
                'tlr_type': 'poster',
                'class_size': 'large',
                'bloom_level': 'understand',
                'budget_band': 'medium',
                'learning_outcome': 'Children will understand seasonal changes, weather patterns, and appropriate responses to environmental changes.',
                'learning_styles': ['Visual Learner', 'Kinesthetic Learner'],
                'special_needs': ['Attention Difficulties', 'Developmental Delays'],
                'themes': ['Weather and Seasons', 'My Environment', 'Festivals and Celebrations']
            }
        ]
        
        for tlr_data in cross_curricular_tlrs:
            self.create_tlr(tlr_data, nursery, lang_subject)

    def create_tlr(self, tlr_data, class_level, subject):
        """Helper method to create TLR objects with all relationships"""
        
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
            
            self.stdout.write(f'Created interactive TLR: {tlr.title}')
        else:
            self.stdout.write(f'TLR already exists: {tlr.title}')