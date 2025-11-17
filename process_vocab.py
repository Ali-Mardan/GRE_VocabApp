#!/usr/bin/env python3
"""Process GRE vocabulary CSV into thematic JSON groups using NLP."""

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
                if num_chunks > 1:
                    chunked_groups[f"{theme_name} {i + 1}"] = chunk
                else:
                    chunked_groups[theme_name] = chunk

    return chunked_groups

def main():
    """Main processing function."""
    print("Reading CSV data...")
    words = read_csv_data()
    print(f"Total words: {len(words)}")

    print("\nCategorizing words into thematic groups...")
    theme_words = categorize_words(words)
    print(f"Initial themes identified: {len(theme_words)}")

    print("\nChunking large groups into ~5 word groups...")
    final_groups = chunk_groups(theme_words, chunk_size=5)
    print(f"Final groups created: {len(final_groups)}")

    # Verify all words are included
    total_words_in_groups = sum(len(words) for words in final_groups.values())
    print(f"\nVerification: {total_words_in_groups} words organized (expected {len(words)})")

    if total_words_in_groups != len(words):
        print("WARNING: Some words may be missing!")

    print("\nSaving to vocab_thematic_groups.json...")
    with open('vocab_thematic_groups.json', 'w', encoding='utf-8') as f:
        json.dump(final_groups, f, indent=2, ensure_ascii=False)

    print("\n✓ Processing complete!")
    print(f"Output saved to: vocab_thematic_groups.json")

    # Print sample groups
    print("\n=== Sample Groups ===")
    for i, (theme, words) in enumerate(list(final_groups.items())[:5]):
        print(f"\n{theme} ({len(words)} words):")
        for word_data in words[:3]:
            print(f"  - {word_data['word']}: {word_data['meaning'][:80]}...")

if __name__ == '__main__':
    main()
