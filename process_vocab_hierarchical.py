#!/usr/bin/env python3
"""Process GRE vocabulary CSV into hierarchical thematic JSON groups."""

import json
import csv
from collections import defaultdict
import re

def read_csv_data():
    """Read and parse CSV data."""
    words = []
    with open('word_meanings.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['Word'].strip()
            meaning = row['Meaning'].strip()
            secondary = row['Secondary_Meaning'].strip()

            # Combine meanings intelligently
            if secondary:
                combined_meaning = f"{meaning} (also) {secondary}"
            else:
                combined_meaning = meaning

            words.append({
                'word': word,
                'meaning': meaning,
                'secondary_meaning': secondary,
                'combined': combined_meaning
            })

    return words

def extract_key_concepts(meaning):
    """Extract key concepts from meanings for thematic grouping."""
    # Define thematic keywords and their categories
    themes = {
        'praise': ['praise', 'admire', 'approve', 'commend', 'laud', 'extol', 'glorify'],
        'criticism': ['criticize', 'condemn', 'denounce', 'scold', 'rebuke', 'reprimand', 'censure', 'attack', 'mock', 'ridicule', 'belittle'],
        'deception': ['deceive', 'trick', 'mislead', 'false', 'fake', 'pretend', 'conceal', 'hide', 'secret'],
        'honesty': ['honest', 'truthful', 'sincere', 'candid', 'frank', 'genuine', 'innocent'],
        'anger': ['angry', 'hostile', 'aggressive', 'irritable', 'rage', 'furious', 'wrathful'],
        'calm': ['calm', 'peaceful', 'tranquil', 'serene', 'composed', 'untroubled'],
        'stubbornness': ['stubborn', 'inflexible', 'obstinate', 'unyielding', 'rigid', 'unwilling to change'],
        'flexibility': ['flexible', 'adaptable', 'yielding', 'compliant', 'willing'],
        'abundance': ['abundant', 'plentiful', 'copious', 'profuse', 'large numbers', 'excessive'],
        'scarcity': ['scarce', 'lacking', 'insufficient', 'meager', 'sparse', 'dearth'],
        'intelligence': ['intelligent', 'wise', 'clever', 'shrewd', 'insightful', 'knowledge', 'learning'],
        'foolishness': ['foolish', 'silly', 'stupid', 'absurd', 'ridiculous', 'immature'],
        'energy': ['energetic', 'enthusiastic', 'passionate', 'vigorous', 'lively', 'eager'],
        'laziness': ['lazy', 'inactive', 'sluggish', 'lethargic', 'idle'],
        'clarity': ['clear', 'transparent', 'lucid', 'understand', 'obvious'],
        'obscurity': ['obscure', 'unclear', 'mysterious', 'difficult to understand', 'hidden'],
        'wealth': ['wealthy', 'rich', 'opulent', 'luxurious', 'prosperous'],
        'poverty': ['poor', 'impoverished', 'destitute', 'penniless'],
        'increase': ['increase', 'grow', 'expand', 'enlarge', 'augment', 'swell'],
        'decrease': ['decrease', 'reduce', 'diminish', 'lessen', 'shrink', 'wane'],
        'temporary': ['temporary', 'brief', 'short', 'fleeting', 'ephemeral', 'transient'],
        'permanent': ['permanent', 'lasting', 'eternal', 'unchanging', 'enduring'],
        'talkative': ['talkative', 'verbose', 'wordy', 'garrulous', 'loquacious'],
        'silent': ['silent', 'quiet', 'taciturn', 'reserved', 'reticent', 'uncommunicative'],
        'friendly': ['friendly', 'pleasant', 'amiable', 'sociable', 'affable', 'genial'],
        'unfriendly': ['unfriendly', 'hostile', 'rude', 'aloof', 'distant', 'cold'],
        'arrogance': ['arrogant', 'proud', 'haughty', 'superior', 'disdainful', 'pompous'],
        'humility': ['humble', 'modest', 'unassuming', 'meek', 'respectful'],
        'courage': ['brave', 'courageous', 'bold', 'fearless', 'daring', 'valiant'],
        'cowardice': ['cowardly', 'fearful', 'timid', 'afraid'],
        'generosity': ['generous', 'giving', 'charitable', 'benevolent', 'altruistic'],
        'stinginess': ['stingy', 'miserly', 'cheap', 'frugal', 'unwilling to spend'],
        'harmful': ['harmful', 'damaging', 'destructive', 'injurious', 'detrimental'],
        'helpful': ['helpful', 'beneficial', 'advantageous', 'favorable'],
        'agreement': ['agree', 'harmony', 'accord', 'consensus', 'compatible'],
        'disagreement': ['disagree', 'conflict', 'discord', 'argument', 'dispute'],
        'complex': ['complex', 'complicated', 'intricate', 'elaborate', 'convoluted'],
        'simple': ['simple', 'plain', 'austere', 'basic', 'straightforward'],
        'support': ['support', 'strengthen', 'reinforce', 'bolster', 'help'],
        'opposition': ['oppose', 'resist', 'obstruct', 'hinder', 'prevent'],
        'beginning': ['begin', 'start', 'new', 'nascent', 'initial'],
        'ending': ['end', 'finish', 'terminate', 'cease', 'conclude'],
        'beauty': ['beautiful', 'attractive', 'pleasant', 'aesthetic', 'charming'],
        'ugliness': ['ugly', 'unattractive', 'unpleasant', 'repulsive'],
        'order': ['orderly', 'organized', 'systematic', 'methodical'],
        'disorder': ['disorderly', 'chaotic', 'confused', 'jumbled', 'messy'],
        'truth': ['true', 'truthful', 'accurate', 'correct', 'valid'],
        'falsehood': ['false', 'untrue', 'incorrect', 'erroneous', 'dishonest'],
        'power': ['powerful', 'strong', 'dominant', 'authoritative'],
        'weakness': ['weak', 'feeble', 'frail', 'powerless'],
        'old': ['old', 'ancient', 'outdated', 'archaic', 'obsolete'],
        'new': ['new', 'novel', 'modern', 'recent', 'fresh'],
        'hard': ['hard', 'difficult', 'challenging', 'arduous'],
        'easy': ['easy', 'simple', 'effortless', 'straightforward'],
        'emotion': ['emotional', 'feeling', 'sentiment', 'passion'],
        'emotionless': ['unemotional', 'impassive', 'stoic', 'indifferent'],
        'strictness': ['strict', 'severe', 'harsh', 'rigorous', 'demanding'],
        'leniency': ['lenient', 'permissive', 'tolerant', 'forgiving'],
        'moral': ['moral', 'ethical', 'virtuous', 'righteous', 'principled'],
        'immoral': ['immoral', 'unethical', 'wicked', 'evil', 'corrupt'],
        'fear': ['fear', 'afraid', 'frightened', 'scared', 'terrified'],
        'confidence': ['confident', 'assured', 'self-assured', 'certain'],
        'happiness': ['happy', 'joyful', 'cheerful', 'delighted', 'pleased'],
        'sadness': ['sad', 'gloomy', 'melancholy', 'mournful', 'sorrowful'],
        'skill': ['skillful', 'adept', 'proficient', 'competent', 'expert'],
        'clumsiness': ['clumsy', 'awkward', 'inept', 'maladroit'],
        'physical': ['physical', 'bodily', 'tangible', 'material'],
        'spiritual': ['spiritual', 'divine', 'sacred', 'holy'],
        'ordinary': ['ordinary', 'common', 'mundane', 'everyday', 'typical'],
        'extraordinary': ['extraordinary', 'unusual', 'remarkable', 'exceptional'],
        'attention': ['attention', 'careful', 'attentive', 'vigilant', 'watchful'],
        'inattention': ['inattentive', 'careless', 'negligent', 'heedless'],
        'relevant': ['relevant', 'pertinent', 'applicable', 'appropriate'],
        'irrelevant': ['irrelevant', 'unrelated', 'extraneous', 'immaterial'],
        'respect': ['respect', 'reverence', 'esteem', 'honor'],
        'disrespect': ['disrespect', 'contempt', 'scorn', 'disdain'],
        'change': ['change', 'alter', 'modify', 'transform'],
        'unchanging': ['unchanging', 'constant', 'stable', 'fixed'],
        'speed': ['fast', 'quick', 'rapid', 'swift', 'hasty'],
        'slowness': ['slow', 'gradual', 'sluggish', 'deliberate'],
        'inclusion': ['include', 'incorporate', 'embrace', 'comprise'],
        'exclusion': ['exclude', 'omit', 'reject', 'banish'],
        'persuasion': ['persuade', 'convince', 'urge', 'encourage'],
        'dissuasion': ['dissuade', 'discourage', 'deter'],
        'acceptance': ['accept', 'receive', 'embrace', 'tolerate'],
        'rejection': ['reject', 'refuse', 'deny', 'spurn'],
        'show': ['show', 'display', 'reveal', 'expose', 'demonstrate'],
        'hide': ['hide', 'conceal', 'obscure', 'cover'],
        'restraint': ['restrain', 'control', 'restrict', 'limit'],
        'freedom': ['free', 'liberate', 'release', 'unrestricted'],
        'necessity': ['necessary', 'essential', 'required', 'vital'],
        'unnecessary': ['unnecessary', 'superfluous', 'redundant', 'excess'],
        'forgiveness': ['forgive', 'pardon', 'absolve', 'exonerate'],
        'blame': ['blame', 'accuse', 'fault', 'condemn'],
        'unity': ['unity', 'together', 'united', 'cohesive'],
        'division': ['divide', 'split', 'separate', 'fragment'],
        'similarity': ['similar', 'alike', 'comparable', 'analogous'],
        'difference': ['different', 'distinct', 'disparate', 'diverse'],
        'certainty': ['certain', 'sure', 'definite', 'unquestionable'],
        'uncertainty': ['uncertain', 'doubtful', 'ambiguous', 'questionable'],
        'praise_quality': ['excellent', 'superior', 'outstanding', 'exemplary'],
        'criticism_quality': ['poor', 'inferior', 'inadequate', 'deficient'],
    }

    meaning_lower = meaning.lower()
    matched_themes = []

    for theme, keywords in themes.items():
        for keyword in keywords:
            if keyword in meaning_lower:
                matched_themes.append(theme)
                break

    return matched_themes if matched_themes else ['general']

def categorize_words(words):
    """Categorize words into thematic groups."""
    theme_words = defaultdict(list)

    for word_data in words:
        # Combine both meanings for thematic analysis
        full_meaning = word_data['meaning']
        if word_data['secondary_meaning']:
            full_meaning += ' ' + word_data['secondary_meaning']

        themes = extract_key_concepts(full_meaning)

        # Use the first (most relevant) theme
        primary_theme = themes[0]

        theme_words[primary_theme].append({
            'word': word_data['word'],
            'meaning': word_data['combined']
        })

    return theme_words

def chunk_groups(theme_words, chunk_size=5):
    """Split large thematic groups into chunks of approximately chunk_size."""
    chunked_groups = {}

    for theme, words in theme_words.items():
        if len(words) <= chunk_size:
            # Keep small groups as is
            theme_name = theme.replace('_', ' ').title()
            chunked_groups[theme_name] = words
        else:
            # Split into chunks
            num_chunks = (len(words) + chunk_size - 1) // chunk_size
            for i in range(num_chunks):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, len(words))
                chunk = words[start:end]

                theme_name = theme.replace('_', ' ').title()
                chunked_groups[f"{theme_name} {i + 1}"] = chunk

    return chunked_groups

def create_hierarchical_structure(flat_groups):
    """Create hierarchical structure by bundling numbered sub-groups under parent categories."""
    hierarchical = {}

    for group_name, words in flat_groups.items():
        # Check if this is a numbered sub-group (e.g., "Criticism 1", "Criticism 2")
        match = re.match(r'^(.+?)\s+(\d+)$', group_name)

        if match:
            # This is a sub-group
            parent_name = match.group(1)
            sub_number = int(match.group(2))

            if parent_name not in hierarchical:
                hierarchical[parent_name] = {
                    'subgroups': {},
                    'total_words': 0
                }

            hierarchical[parent_name]['subgroups'][f"Part {sub_number}"] = words
            hierarchical[parent_name]['total_words'] += len(words)
        else:
            # This is a standalone group (no sub-groups)
            hierarchical[group_name] = {
                'subgroups': {
                    'All': words
                },
                'total_words': len(words)
            }

    return hierarchical

def print_statistics(hierarchical):
    """Print statistics for the hierarchical structure."""
    print("\n" + "="*80)
    print("HIERARCHICAL VOCABULARY ORGANIZATION STATISTICS")
    print("="*80)

    # Overall statistics
    total_parent_groups = len(hierarchical)
    total_subgroups = sum(len(data['subgroups']) for data in hierarchical.values())
    total_words = sum(data['total_words'] for data in hierarchical.values())

    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Total Parent Categories: {total_parent_groups}")
    print(f"   Total Sub-groups: {total_subgroups}")
    print(f"   Total Words: {total_words}")
    print(f"   Average words per parent category: {total_words / total_parent_groups:.1f}")

    # Detailed breakdown
    print(f"\n📋 DETAILED BREAKDOWN BY PARENT CATEGORY:")
    print(f"{'='*80}")

    # Sort by total words (descending)
    sorted_groups = sorted(hierarchical.items(), key=lambda x: x[1]['total_words'], reverse=True)

    for parent_name, data in sorted_groups:
        num_subgroups = len(data['subgroups'])
        total_words_in_category = data['total_words']

        # Only show "All" label for single-subgroup categories, otherwise show subgroup count
        if num_subgroups == 1 and 'All' in data['subgroups']:
            subgroup_info = "1 group"
        else:
            subgroup_info = f"{num_subgroups} parts"

        print(f"\n{parent_name:.<50} {total_words_in_category:>3} words ({subgroup_info})")

        # Show sub-group breakdown for multi-part categories
        if num_subgroups > 1:
            for subgroup_name, words in sorted(data['subgroups'].items()):
                print(f"   └─ {subgroup_name}: {len(words)} words")

    # Category size distribution
    print(f"\n📈 CATEGORY SIZE DISTRIBUTION:")
    print(f"{'='*80}")

    size_ranges = {
        '1-5 words': 0,
        '6-10 words': 0,
        '11-20 words': 0,
        '21-30 words': 0,
        '31-50 words': 0,
        '50+ words': 0
    }

    for data in hierarchical.values():
        count = data['total_words']
        if count <= 5:
            size_ranges['1-5 words'] += 1
        elif count <= 10:
            size_ranges['6-10 words'] += 1
        elif count <= 20:
            size_ranges['11-20 words'] += 1
        elif count <= 30:
            size_ranges['21-30 words'] += 1
        elif count <= 50:
            size_ranges['31-50 words'] += 1
        else:
            size_ranges['50+ words'] += 1

    for range_name, count in size_ranges.items():
        if count > 0:
            print(f"   {range_name:.<20} {count:>3} categories")

    print(f"\n{'='*80}\n")

def main():
    """Main processing function."""
    print("Reading CSV data...")
    words = read_csv_data()
    print(f"Total words: {len(words)}")

    print("\nCategorizing words into thematic groups...")
    theme_words = categorize_words(words)
    print(f"Initial themes identified: {len(theme_words)}")

    print("\nChunking large groups into ~5 word groups...")
    flat_groups = chunk_groups(theme_words, chunk_size=5)
    print(f"Flat groups created: {len(flat_groups)}")

    print("\nCreating hierarchical structure...")
    hierarchical = create_hierarchical_structure(flat_groups)

    # Print statistics
    print_statistics(hierarchical)

    # Save both formats
    print("Saving hierarchical structure to vocab_hierarchical.json...")
    with open('vocab_hierarchical.json', 'w', encoding='utf-8') as f:
        json.dump(hierarchical, f, indent=2, ensure_ascii=False)

    print("Saving flat structure to vocab_thematic_groups.json...")
    with open('vocab_thematic_groups.json', 'w', encoding='utf-8') as f:
        json.dump(flat_groups, f, indent=2, ensure_ascii=False)

    print("\n✓ Processing complete!")
    print(f"   - Hierarchical output: vocab_hierarchical.json")
    print(f"   - Flat output: vocab_thematic_groups.json")

if __name__ == '__main__':
    main()
