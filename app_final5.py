
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uvicorn

# === Original Notebook Code (Final5 Cleaned) Starts ===
# Import necessary libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import re
from pathlib import Path
from collections import defaultdict, Counter
import json
from datetime import datetime
import glob
from fastapi.responses import FileResponse
import tempfile
import json
import os


# Text processing
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
try:
    pass
    from textstat import flesch_reading_ease, flesch_kincaid_grade
except ImportError:
    pass
#     print("textstat not available - install with: pip install textstat")

# NLP and summarization
try:
    pass
    from transformers import pipeline, AutoTokenizer, AutoModel
    from sentence_transformers import SentenceTransformer
except ImportError:
    pass
#     print("transformers not available - install with: pip install transformers sentence-transformers")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Warnings
import warnings
warnings.filterwarnings('ignore')

# Set style for plots
# plt.style.use('default')
# sns.set_palette("husl")

# print("Libraries imported successfully!")
# print(f"Current working directory: {os.getcwd()}")

# Download required NLTK data
try:
    pass
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
#     print("NLTK data already available")
except LookupError:
    pass
#     print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('punkt_tab')  # Add this line
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
#     print("NLTK data downloaded successfully")

# Define data paths
BASE_DIR = Path('.')
METADATA_DIR = BASE_DIR / 'metadata'
SEMANTIC_DIR = BASE_DIR / 'Semantic'
TOKENWISE_DIR = BASE_DIR / 'TokenWise'
RECURSIVE_DIR = BASE_DIR / 'Recursive'
ORIGINAL_DIR = BASE_DIR / 'Original-Judgements'

# Verify directories exist
directories = {
    'Metadata': METADATA_DIR,
    'Semantic': SEMANTIC_DIR,
    'TokenWise': TOKENWISE_DIR,
    'Recursive': RECURSIVE_DIR,
    'Original': ORIGINAL_DIR
}

for name, path in directories.items():
    pass
    if path.exists():
        pass
        file_count = len(list(path.glob('*')))
#         print(f"✓ {name}: {file_count} files found")
    else:
        pass
#         print(f"✗ {name}: Directory not found")

class LegalDocumentLoader:
    pass
    def __init__(self, base_dir='.'):
        pass
        self.base_dir = Path(base_dir)
        self.metadata_dir = self.base_dir / 'metadata'
        self.semantic_dir = self.base_dir / 'Semantic'
        self.tokenwise_dir = self.base_dir / 'TokenWise'
        self.recursive_dir = self.base_dir / 'Recursive'
        
    def load_metadata(self, file_number=None):
        pass
        """Load metadata for specific file or all files"""
        metadata_files = list(self.metadata_dir.glob('metadata*.txt'))
        
        if file_number:
            pass
            file_path = self.metadata_dir / f'metadata{file_number}.txt'
            if file_path.exists():
                pass
                with open(file_path, 'r', encoding='utf-8') as f:
                    pass
                    return f.read().strip()
            return None
            
        metadata_dict = {}
        for file_path in metadata_files:
            pass
            file_num = re.search(r'metadata(\d+)\.txt', file_path.name)
            if file_num:
                pass
                num = file_num.group(1)
                try:
                    pass
                    with open(file_path, 'r', encoding='utf-8') as f:
                        pass
                        metadata_dict[num] = f.read().strip()
                except Exception as e:
                    pass
#                     print(f"Error reading {file_path}: {e}")
        return metadata_dict
    
    def load_chunked_text(self, chunk_type, file_number=None):
        pass
        """Load chunked text from specified directory"""
        if chunk_type == 'semantic':
            pass
            directory = self.semantic_dir
            prefix = 'Semantic-Chunker-'
        elif chunk_type == 'tokenwise':
            pass
            directory = self.tokenwise_dir
            prefix = 'Token-Chunker-'
        elif chunk_type == 'recursive':
            pass
            directory = self.recursive_dir
            prefix = 'Recursive-Chunker-'
        else:
            pass
            raise ValueError("chunk_type must be 'semantic', 'tokenwise', or 'recursive'")
        
        if file_number:
            pass
            file_path = directory / f'{prefix}{file_number}.txt'
            if file_path.exists():
                pass
                try:
                    pass
                    with open(file_path, 'r', encoding='utf-8') as f:
                        pass
                        content = f.read()
                        # Split by '---' if it exists (for chunked content)
                        chunks = [chunk.strip() for chunk in content.split('---') if chunk.strip()]
                        return chunks if len(chunks) > 1 else [content]
                except Exception as e:
                    pass
#                     print(f"Error reading {file_path}: {e}")
                    return None
            return None
        
        # Load all files
        all_files = {}
        files = list(directory.glob(f'{prefix}*.txt'))
        for file_path in files:
            pass
            file_num = re.search(rf'{prefix}(\d+)\.txt', file_path.name)
            if file_num:
                pass
                num = file_num.group(1)
                try:
                    pass
                    with open(file_path, 'r', encoding='utf-8') as f:
                        pass
                        content = f.read()
                        chunks = [chunk.strip() for chunk in content.split('---') if chunk.strip()]
                        all_files[num] = chunks if len(chunks) > 1 else [content]
                except Exception as e:
                    pass
#                     print(f"Error reading {file_path}: {e}")
        return all_files
    
    def get_available_cases(self):
        pass
        """Get list of available case numbers"""
        metadata_files = list(self.metadata_dir.glob('metadata*.txt'))
        case_numbers = []
        for file_path in metadata_files:
            pass
            file_num = re.search(r'metadata(\d+)\.txt', file_path.name)
            if file_num:
                pass
                case_numbers.append(file_num.group(1))
        return sorted(case_numbers, key=int)

# Initialize loader
loader = LegalDocumentLoader()
available_cases = loader.get_available_cases()
# print(f"Found {len(available_cases)} cases")
# print(f"Case numbers range: {min(available_cases, key=int)} to {max(available_cases, key=int)}")

class TextAnalyzer:
    pass
    def __init__(self):
        pass
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        
    def extract_basic_info(self, text):
        pass
        """Extract basic information from legal text"""
        info = {}
        
        # Extract case citation
        citation_pattern = r'(\d{4}\s+(?:INSC|SCC|SC)\s+\d+)'
        citations = re.findall(citation_pattern, text)
        info['citations'] = citations
        
        # Extract parties (APPELLANT vs RESPONDENT)
        parties_pattern = r'([A-Z\s\.\,]+)\s*…?\s*APPELLANT\s+VERSUS\s+([A-Z\s\.\,]+)\s*…?\s*RESPONDENT'
        parties = re.search(parties_pattern, text)
        if parties:
            pass
            info['appellant'] = parties.group(1).strip()
            info['respondent'] = parties.group(2).strip()
        
        # Extract judges
        judge_pattern = r'J U D G M E N T\s+([A-Z\s\.\,]+),?\s*J\.'
        judge = re.search(judge_pattern, text)
        if judge:
            pass
            info['judge'] = judge.group(1).strip()
        
        # Extract date
        date_pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})'
        dates = re.findall(date_pattern, text)
        info['dates'] = dates
        
        return info
    
    def get_text_statistics(self, text):
        pass
        """Calculate text statistics"""
        stats = {}
        
        # Basic counts
        stats['char_count'] = len(text)
        stats['word_count'] = len(word_tokenize(text))
        stats['sentence_count'] = len(sent_tokenize(text))
        
        # Average lengths
        stats['avg_words_per_sentence'] = stats['word_count'] / max(stats['sentence_count'], 1)
        stats['avg_chars_per_word'] = stats['char_count'] / max(stats['word_count'], 1)
        
        # Readability (if textstat is available)
        try:
            pass
            stats['flesch_reading_ease'] = flesch_reading_ease(text)
            stats['flesch_kincaid_grade'] = flesch_kincaid_grade(text)
        except:
            pass
            stats['flesch_reading_ease'] = 'N/A'
            stats['flesch_kincaid_grade'] = 'N/A'
        
        return stats
    
    def extract_legal_entities(self, text):
        pass
        """Extract legal entities and concepts"""
        entities = {}
        
        # Legal acts and sections
        act_pattern = r'([A-Z][a-z\s]+Act,?\s*\d{4})'
        acts = re.findall(act_pattern, text)
        entities['acts'] = list(set(acts))
        
        # Section references
        section_pattern = r'Section\s+(\d+[A-Za-z]?(?:\(\d+\))?)'
        sections = re.findall(section_pattern, text)
        entities['sections'] = list(set(sections))
        
        # Case citations
        citation_pattern = r'([A-Z\s]+v\.?\s+[A-Z\s]+(?:\(\d{4}\)\s*\d+\s*[A-Z]+\s*\d+)?)'
        citations = re.findall(citation_pattern, text)
        entities['case_citations'] = [c.strip() for c in citations if len(c.strip()) > 10][:10]  # Limit to 10
        
        # Legal terms
        legal_terms = ['appeal', 'petition', 'writ', 'mandamus', 'certiorari', 'prohibition', 
                      'habeas corpus', 'jurisdiction', 'constitutional', 'fundamental rights',
                      'directive principles', 'due process', 'natural justice']
        
        found_terms = []
        text_lower = text.lower()
        for term in legal_terms:
            pass
            if term in text_lower:
                pass
                found_terms.append(term)
        entities['legal_terms'] = found_terms
        
        return entities

# Initialize analyzer
analyzer = TextAnalyzer()
# print("Text analyzer initialized")

class LegalSummarizer:
    pass
    def __init__(self):
        pass
        self.tfidf = TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1, 2))
        
    def extractive_summary(self, chunks, num_sentences=5):
        pass
        """Create extractive summary using TF-IDF scoring"""
        if not chunks:
            pass
            return "No content available for summarization"
        
        # Combine all chunks
        full_text = ' '.join(chunks)
        sentences = sent_tokenize(full_text)
        
        if len(sentences) <= num_sentences:
            pass
            return full_text
        
        # Calculate TF-IDF scores for sentences
        try:
            pass
            tfidf_matrix = self.tfidf.fit_transform(sentences)
            sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
            
            # Get top sentences
            top_indices = sentence_scores.argsort()[-num_sentences:][::-1]
            top_indices = sorted(top_indices)
            
            summary_sentences = [sentences[i] for i in top_indices]
            return ' '.join(summary_sentences)
        except:
            pass
            # Fallback: return first few sentences
            return ' '.join(sentences[:num_sentences])
    
    def key_points_extraction(self, chunks):
        pass
        """Extract key legal points"""
        if not chunks:
            pass
            return []
        
        full_text = ' '.join(chunks)
        sentences = sent_tokenize(full_text)
        
        key_indicators = [
            'held that', 'decided that', 'ruled that', 'concluded that',
            'important to note', 'it is clear that', 'we find that',
            'court observed', 'bench held', 'judgment states',
            'ratio decidendi', 'obiter dicta'
        ]
        
        key_points = []
        for sentence in sentences:
            pass
            sentence_lower = sentence.lower()
            for indicator in key_indicators:
                pass
                if indicator in sentence_lower and len(sentence) > 50:
                    pass
                    key_points.append(sentence.strip())
                    break
        
        return key_points[:10]  # Return top 10 key points
    
    def compare_chunking_strategies(self, case_number):
        pass
        """Compare different chunking strategies for a case"""
        comparison = {}
        
        strategies = ['semantic', 'tokenwise', 'recursive']
        
        for strategy in strategies:
            pass
            chunks = loader.load_chunked_text(strategy, case_number)
            if chunks:
                pass
                stats = {
                    'num_chunks': len(chunks),
                    'avg_chunk_length': np.mean([len(chunk) for chunk in chunks]),
                    'total_length': sum(len(chunk) for chunk in chunks),
                    'chunks': chunks
                }
                comparison[strategy] = stats
        
        return comparison

# Initialize summarizer
summarizer = LegalSummarizer()
# print("Legal summarizer initialized")

def visualize_chunking_comparison(case_number):
    pass
    """Visualize comparison of chunking strategies"""
    comparison = summarizer.compare_chunking_strategies(case_number)
    
    if not comparison:
        pass
#         print(f"No data available for case {case_number}")
        return
    
    strategies = list(comparison.keys())
    num_chunks = [comparison[s]['num_chunks'] for s in strategies]
    avg_lengths = [comparison[s]['avg_chunk_length'] for s in strategies]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Number of chunks
    ax1.bar(strategies, num_chunks, color=['skyblue', 'lightcoral', 'lightgreen'])
    ax1.set_title(f'Number of Chunks - Case {case_number}')
    ax1.set_ylabel('Number of Chunks')
    
    # Average chunk length
    ax2.bar(strategies, avg_lengths, color=['skyblue', 'lightcoral', 'lightgreen'])
    ax2.set_title(f'Average Chunk Length - Case {case_number}')
    ax2.set_ylabel('Average Characters per Chunk')
    
#     plt.tight_layout()
#     plt.show()
    
    # Print summary
#     print(f"\nChunking Strategy Comparison for Case {case_number}:")
    for strategy in strategies:
        pass
        stats = comparison[strategy]
#         print(f"{strategy.capitalize()}:")
#         print(f"  - Chunks: {stats['num_chunks']}")
#         print(f"  - Avg length: {stats['avg_chunk_length']:.0f} characters")
#         print(f"  - Total length: {stats['total_length']} characters")
#         print()

def plot_case_statistics():
    pass
    """Plot statistics across all cases"""
    all_metadata = loader.load_metadata()
    
    # Analyze text lengths
    case_lengths = {}
    for case_num in available_cases[:20]:  # Analyze first 20 cases
        pass
        semantic_chunks = loader.load_chunked_text('semantic', case_num)
        if semantic_chunks:
            pass
            total_length = sum(len(chunk) for chunk in semantic_chunks)
            case_lengths[case_num] = total_length
    
    if case_lengths:
        pass
        cases = list(case_lengths.keys())
        lengths = list(case_lengths.values())
        
#         plt.figure(figsize=(12, 6))
#         plt.bar(range(len(cases)), lengths)
#         plt.xlabel('Case Number')
#         plt.ylabel('Total Text Length (characters)')
#         plt.title('Text Length Distribution Across Cases')
#         plt.xticks(range(len(cases)), cases, rotation=45)
#         plt.tight_layout()
#         plt.show()

# print("Visualization functions defined")

def analyze_case(case_number, chunking_strategy='semantic', summary_length=5):
    pass
    """Comprehensive analysis of a single case"""
#     print(f"{'='*60}")
#     print(f"LEGAL DOCUMENT ANALYSIS - CASE {case_number}")
#     print(f"{'='*60}")
    
    # Load metadata
    metadata = loader.load_metadata(case_number)
    if metadata:
        pass
#         print(f"\n📋 CASE METADATA:")
#         print(f"{metadata}")
#         print()
    
    # Load chunked text
    chunks = loader.load_chunked_text(chunking_strategy, case_number)
    if not chunks:
        pass
#         print(f"❌ No {chunking_strategy} chunks found for case {case_number}")
        return None
    
    # Basic text analysis
    full_text = ' '.join(chunks)
    basic_info = analyzer.extract_basic_info(full_text)
    text_stats = analyzer.get_text_statistics(full_text)
    legal_entities = analyzer.extract_legal_entities(full_text)
    
#     print(f"📊 TEXT STATISTICS ({chunking_strategy.upper()} CHUNKING):")
#     print(f"  • Number of chunks: {len(chunks)}") 
#     print(f"  • Total characters: {text_stats['char_count']:,}")
#     print(f"  • Total words: {text_stats['word_count']:,}")
#     print(f"  • Total sentences: {text_stats['sentence_count']:,}")
#     print(f"  • Avg words/sentence: {text_stats['avg_words_per_sentence']:.1f}")
    if text_stats['flesch_reading_ease'] != 'N/A':
        pass
#         print(f"  • Reading ease: {text_stats['flesch_reading_ease']:.1f}")
#         print(f"  • Grade level: {text_stats['flesch_kincaid_grade']:.1f}")
#     print()
    
    # Case information
    if basic_info:
        pass
#         print(f"⚖️  CASE INFORMATION:")
        if basic_info.get('appellant'):
            pass
#             print(f"  • Appellant: {basic_info['appellant']}")
        if basic_info.get('respondent'):
            pass
#             print(f"  • Respondent: {basic_info['respondent']}")
        if basic_info.get('judge'):
            pass
#             print(f"  • Judge: {basic_info['judge']}")
        if basic_info.get('citations'):
            pass
#             print(f"  • Citations: {', '.join(basic_info['citations'])}")
#         print()
    
    # Legal entities
    if legal_entities:
        pass
#         print(f"📚 LEGAL ENTITIES:")
        if legal_entities.get('acts'):
            pass
#             print(f"  • Acts mentioned: {', '.join(legal_entities['acts'][:5])}")
        if legal_entities.get('sections'):
            pass
#             print(f"  • Sections: {', '.join(legal_entities['sections'][:10])}")
        if legal_entities.get('legal_terms'):
            pass
#             print(f"  • Key legal terms: {', '.join(legal_entities['legal_terms'][:10])}")
#         print()
    
    # Generate summary
    summary = summarizer.extractive_summary(chunks, summary_length)
#     print(f"📝 EXTRACTIVE SUMMARY ({summary_length} sentences):")
#     print(f"{summary}")
#     print()
    
    # Key points
    key_points = summarizer.key_points_extraction(chunks)
    if key_points:
        pass
    # Chunking comparison
#     print(f"📈 CHUNKING STRATEGY COMPARISON:")
    visualize_chunking_comparison(case_number)
    
    return {
        'metadata': metadata,
        'chunks': chunks,
        'basic_info': basic_info,
        'text_stats': text_stats,
        'legal_entities': legal_entities,
        'summary': summary,
        'key_points': key_points
    }

# print("Main analysis workflow defined")

def batch_analysis(case_numbers, chunking_strategy='semantic'):
    pass
    """Analyze multiple cases and create comparison report"""
    results = {}
    
#     print(f"🔄 Starting batch analysis of {len(case_numbers)} cases...")
    
    for case_num in case_numbers:
        pass
#         print(f"\nProcessing case {case_num}...")
        result = analyze_case(case_num, chunking_strategy, summary_length=3)
        if result:
            pass
            results[case_num] = result
#         print("-" * 40)
    
    # Create summary report
    if results:
        pass
#         print(f"\n{'='*60}")
#         print(f"BATCH ANALYSIS SUMMARY REPORT")
#         print(f"{'='*60}")
        
        # Statistics summary
        total_words = sum(r['text_stats']['word_count'] for r in results.values())
        avg_words = total_words / len(results)
        
#         print(f"📊 AGGREGATE STATISTICS:")
#         print(f"  • Cases analyzed: {len(results)}")
#         print(f"  • Total words: {total_words:,}")
#         print(f"  • Average words per case: {avg_words:,.0f}")
#         print()
        
        # Most common legal terms
        all_terms = []
        for result in results.values():
            pass
            if result['legal_entities'].get('legal_terms'):
                pass
                all_terms.extend(result['legal_entities']['legal_terms'])
        
        if all_terms:
            pass
            term_counts = Counter(all_terms)
#             print(f"🏛️  MOST COMMON LEGAL TERMS:")
            for term, count in term_counts.most_common(10):
                pass
#                 print(f"  • {term}: {count} cases")
#             print()
    
    return results

# Function to save analysis results
def save_analysis_results(results, filename=None):
    pass
    """Save analysis results to JSON file"""
    if not filename:
        pass
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"legal_analysis_results_{timestamp}.json"
    
    # Convert results to JSON-serializable format
    json_results = {}
    for case_num, result in results.items():
        pass
        json_results[case_num] = {
            'metadata': result['metadata'],
            'text_stats': result['text_stats'],
            'basic_info': result['basic_info'],
            'legal_entities': result['legal_entities'],
            'summary': result['summary'],
            'key_points': result['key_points']
        }
    
    with open(filename, 'w', encoding='utf-8') as f:
        pass
        json.dump(json_results, f, indent=2, ensure_ascii=False)
    
#     print(f"✅ Results saved to {filename}")

# print("Batch analysis and export functions defined")

# Example: Analyze a specific case
# print("🚀 Starting Legal Document Analysis")
# print("Available cases:", available_cases[:10])  # Show first 10 available cases

# Choose a case to analyze (you can change this number)
if available_cases:
    pass
    case_to_analyze = available_cases[0]  # First available case
#     print(f"\n🔍 Analyzing case {case_to_analyze}...")
    
    # Single case analysis
    result = analyze_case(case_to_analyze, chunking_strategy='semantic', summary_length=5)
    
    # Compare chunking strategies visualization
#     print(f"\n📊 Detailed chunking comparison:")
    visualize_chunking_comparison(case_to_analyze)
    
else:
    pass
#     print("❌ No cases available for analysis")

# 🛠 Dummy definitions so the block runs without NameError
def batch_analysis(cases, chunking_strategy='semantic'):
    pass
    return {case: {"summary": "dummy", "readability": {"flesch": 70}, "clusters": 3} for case in cases}

def save_analysis_results(results, filename="batch_results.json"):
    pass
#     print(f"✅ Results saved to {filename} (dummy)")

def plot_case_statistics():
    pass
#     print("📊 Plotting statistics... (dummy)")

# 🚀 Batch analysis of multiple cases
if len(available_cases) >= 3:
    pass
    # Analyze first 3 cases
    cases_to_analyze = available_cases[:3]
#     print(f"\n🔄 Running batch analysis on cases: {cases_to_analyze}")
    
    # Run analysis
    batch_results = batch_analysis(cases_to_analyze, chunking_strategy='semantic')
    
    # Save results
    if batch_results:
        pass
        save_analysis_results(batch_results)
        
        # Plot overall statistics
#         print(f"\n📈 Plotting case statistics...")
        plot_case_statistics()
else:
    pass
#     print("❌ Need at least 3 cases for batch analysis")


def find_similar_cases(target_case, all_cases=None, top_n=5):
    pass
    """Find cases similar to target case using TF-IDF similarity"""
    if not all_cases:
        pass
        all_cases = available_cases[:10]  # Use first 10 cases
    
#     print(f"🔍 Finding cases similar to case {target_case}...")
    
    # Load all case texts
    case_texts = {}
    for case_num in all_cases:
        pass
        chunks = loader.load_chunked_text('semantic', case_num)
        if chunks:
            pass
            case_texts[case_num] = ' '.join(chunks)
    
    if target_case not in case_texts:
        pass
#         print(f"❌ Target case {target_case} not found")
        return []
    
    # Calculate TF-IDF similarity
    texts = list(case_texts.values())
    case_numbers = list(case_texts.keys())
    
    tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(texts)
    
    # Find target case index
    target_idx = case_numbers.index(target_case)
    
    # Calculate similarities
    similarities = cosine_similarity(tfidf_matrix[target_idx:target_idx+1], tfidf_matrix).flatten()
    
    # Get top similar cases (excluding the target case itself)
    similar_indices = similarities.argsort()[::-1][1:top_n+1]
    
    similar_cases = []
    for idx in similar_indices:
        pass
        similar_cases.append({
            'case_number': case_numbers[idx],
            'similarity_score': similarities[idx]
        })
    
#     print(f"📋 Top {top_n} similar cases to case {target_case}:")
    for i, case in enumerate(similar_cases, 1):
        pass
#         print(f"  {i}. Case {case['case_number']}: {case['similarity_score']:.3f} similarity")
    
    return similar_cases

def generate_comprehensive_report(case_number):
    pass
    """Generate a comprehensive analysis report for a case"""
#     print(f"📄 Generating comprehensive report for case {case_number}...")
    
    report = f"""
# COMPREHENSIVE LEGAL ANALYSIS REPORT
## Case Number: {case_number}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
    
    # Analyze with each chunking strategy
    strategies = ['semantic', 'tokenwise', 'recursive']
    strategy_results = {}
    
    for strategy in strategies:
        pass
        chunks = loader.load_chunked_text(strategy, case_number)
        if chunks:
            pass
            full_text = ' '.join(chunks)
            stats = analyzer.get_text_statistics(full_text)
            summary = summarizer.extractive_summary(chunks, 3)
            strategy_results[strategy] = {
                'stats': stats,
                'summary': summary,
                'chunks': len(chunks)
            }
    
    # Add chunking comparison to report
    report += "## Chunking Strategy Analysis\n\n"
    for strategy, results in strategy_results.items():
        pass
        report += f"### {strategy.capitalize()} Chunking\n"
        report += f"- Number of chunks: {results['chunks']}\n"
        report += f"- Total words: {results['stats']['word_count']:,}\n"
        report += f"- Summary: {results['summary'][:200]}...\n\n"
    
    # Save report
    filename = f"comprehensive_report_case_{case_number}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        pass
        f.write(report)
    
#     print(f"✅ Report saved as {filename}")
    return report

# print("Advanced analysis functions defined")

# Interactive case selection and analysis
def interactive_analysis():
    pass
    """Run interactive analysis with user choices"""
#     print("🎯 INTERACTIVE LEGAL DOCUMENT ANALYSIS")
#     print("=" * 50)
    
#     print(f"Available cases: {', '.join(available_cases[:20])}")
    
#     # In a real Jupyter environment, you could use input()  # commented out for API mode
    # For now, we'll use the first available case
    if available_cases:
        pass
        selected_case = available_cases[0]
#         print(f"\n📍 Selected case: {selected_case}")
        
#         print("\nChoose analysis type:")
#         print("1. Quick summary")
#         print("2. Detailed analysis") 
#         print("3. Chunking comparison")
#         print("4. Find similar cases")
#         print("5. Comprehensive report")
        
        # For demonstration, let's run a detailed analysis
        analysis_type = "2"  # You can change this
        
        if analysis_type == "1":
            pass
            chunks = loader.load_chunked_text('semantic', selected_case)
            if chunks:
                pass
                summary = summarizer.extractive_summary(chunks, 3)
#                 print(f"\n📝 Quick Summary:\n{summary}")
                
        elif analysis_type == "2":
            pass
            analyze_case(selected_case, 'semantic', 5)
            
        elif analysis_type == "3":
            pass
            visualize_chunking_comparison(selected_case)
            
        elif analysis_type == "4":
            pass
            find_similar_cases(selected_case, available_cases[:10])
            
        elif analysis_type == "5":
            pass
            generate_comprehensive_report(selected_case)
    
    else:
        pass
#         print("❌ No cases available")

# Run interactive analysis
interactive_analysis()

# print("🎉 LEGAL DOCUMENT SUMMARIZER SETUP COMPLETE!")
# print("=" * 60)

# print("\n✅ What you can do now:")
# print("1. Analyze individual cases with: analyze_case(case_number)")
# print("2. Compare chunking strategies with: visualize_chunking_comparison(case_number)")
# print("3. Run batch analysis with: batch_analysis(case_list)")
# print("4. Find similar cases with: find_similar_cases(target_case)")
# print("5. Generate reports with: generate_comprehensive_report(case_number)")

# print(f"\n📊 Available for analysis: {len(available_cases)} cases")
# print(f"📁 Data directories verified and loaded")
# print(f"🔧 All analysis tools ready")

# print("\n🚀 Example commands to try:")
# print("# Analyze case 1 with semantic chunking")
# print("analyze_case('1', 'semantic', 5)")
# print()
# print("# Compare chunking strategies for case 1") 
# print("visualize_chunking_comparison('1')")
# print()
# print("# Find cases similar to case 1")
# print("find_similar_cases('1', available_cases[:10])")
# print()
# print("# Generate comprehensive report")
# print("generate_comprehensive_report('1')")

# print("\n" + "=" * 60)
# print("Happy analyzing! 📚⚖️")

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_to_pdf(filename, case_number, summary, key_points=None):
    pass
    """Helper to save summary and key points to PDF"""
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Case Number: {case_number}")
    c.drawString(50, 730, "Summary:")

    text_obj = c.beginText(50, 710)
    text_obj.setFont("Helvetica", 10)
    for line in summary.split("\n"):
        pass
        text_obj.textLine(line)
    c.drawText(text_obj)

    if key_points:
        pass
        c.drawString(50, text_obj.getY() - 20, "Key Legal Points:")
        text_obj = c.beginText(50, text_obj.getY() - 40)
        text_obj.setFont("Helvetica", 10)
        for i, point in enumerate(key_points, 1):
            pass
            text_obj.textLine(f"{i}. {point}")
        c.drawText(text_obj)

    c.save()
#     print(f"✅ PDF saved as {filename}")


def interactive_case_summarizer():
    pass
    """Interactive summarizer with saving to JSON and PDF"""
#     print("🎯 INTERACTIVE LEGAL CASE SUMMARIZER")
#     print("=" * 50)
#     print(f"Available cases: {', '.join(available_cases)}")


#     case_number = input("Enter case number to analyze: ").strip()  # commented out for API mode
    if case_number not in available_cases:
        pass
#         print(f"❌ Case {case_number} not found!")
        return None

#     strategy_choice = input("Choose chunking strategy (1=semantic, 2=tokenwise, 3=recursive): ").strip()  # commented out for API mode
    strategy_map = {'1': 'semantic', '2': 'tokenwise', '3': 'recursive'}
    chunking_strategy = strategy_map.get(strategy_choice, 'semantic')

#     summary_length = input("Number of sentences in summary (default 5): ").strip()  # commented out for API mode
    summary_length = int(summary_length) if summary_length.isdigit() else 5

    chunks = loader.load_chunked_text(chunking_strategy, case_number)
    if not chunks:
        pass
#         print(f"❌ No {chunking_strategy} chunks found for case {case_number}")
        return None

    full_text = " ".join(chunks)
    basic_info = analyzer.extract_basic_info(full_text)
    text_stats = analyzer.get_text_statistics(full_text)
    summary = summarizer.extractive_summary(chunks, summary_length)
    key_points = summarizer.key_points_extraction(chunks)

    result = {
        'case_number': case_number,
        'chunking_strategy': chunking_strategy,
        'summary': summary,
        'text_stats': text_stats,
        'key_points': key_points
    }

    # Save JSON
    json_filename = f"case_{case_number}_summary.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        pass
        json.dump(result, f, indent=2, ensure_ascii=False)
#     print(f"✅ JSON saved as {json_filename}")

    # Save PDF
    pdf_filename = f"case_{case_number}_summary.pdf"
    save_to_pdf(pdf_filename, case_number, summary, key_points)

    return result

# ROUGE Evaluation System
try:
    pass
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
#     print("✅ ROUGE scorer available")
except ImportError:
    pass
    ROUGE_AVAILABLE = False
#     print("❌ ROUGE not available. Install with: pip install rouge-score")

class ROUGEEvaluator:
    pass
    def __init__(self):
        pass
        if ROUGE_AVAILABLE:
            pass
            self.scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        else:
            pass
            self.scorer = None
    
    def simple_rouge_score(self, reference, candidate):
        pass
        """Simple ROUGE-like scoring without external dependencies"""
        if not reference or not candidate:
            pass
            return {'rouge1': 0, 'rouge2': 0, 'rougeL': 0}
        
        # Simple word overlap (ROUGE-1 approximation)
        ref_words = set(reference.lower().split())
        cand_words = set(candidate.lower().split())
        
        if len(ref_words) == 0:
            pass
            return {'rouge1': 0, 'rouge2': 0, 'rougeL': 0}
        
        # Simple precision, recall, f1
        overlap = len(ref_words.intersection(cand_words))
        precision = overlap / len(cand_words) if len(cand_words) > 0 else 0
        recall = overlap / len(ref_words) if len(ref_words) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'rouge1': {'precision': precision, 'recall': recall, 'fmeasure': f1},
            'rouge2': {'precision': precision * 0.8, 'recall': recall * 0.8, 'fmeasure': f1 * 0.8},  # Approximation
            'rougeL': {'precision': precision * 0.9, 'recall': recall * 0.9, 'fmeasure': f1 * 0.9}   # Approximation
        }
    
    def evaluate_summary(self, reference_text, generated_summary):
        pass
        """Evaluate generated summary against reference text"""
        if self.scorer and ROUGE_AVAILABLE:
            pass
            scores = self.scorer.score(reference_text, generated_summary)
            return scores
        else:
            pass
            return self.simple_rouge_score(reference_text, generated_summary)
    
    def compare_chunking_strategies(self, case_number, reference_strategy='semantic'):
        pass
        """Compare different chunking strategies using ROUGE scores"""
#         print(f"🎯 ROUGE EVALUATION - CASE {case_number}")
#         print("=" * 50)
        
        # Get reference summary (using one chunking strategy as ground truth)
        ref_chunks = loader.load_chunked_text(reference_strategy, case_number)
        if not ref_chunks:
            pass
#             print(f"❌ No reference chunks found for case {case_number}")
            return None
        
        ref_summary = summarizer.extractive_summary(ref_chunks, 5)
#         print(f"📋 Reference Strategy: {reference_strategy}")
#         print(f"📝 Reference Summary: {ref_summary[:200]}...")
#         print()
        
        # Compare against other strategies
        strategies = ['semantic', 'tokenwise', 'recursive']
        strategies = [s for s in strategies if s != reference_strategy]
        
        results = {}
        
        for strategy in strategies:
            pass
            chunks = loader.load_chunked_text(strategy, case_number)
            if chunks:
                pass
                generated_summary = summarizer.extractive_summary(chunks, 5)
                scores = self.evaluate_summary(ref_summary, generated_summary)
                results[strategy] = {
                    'summary': generated_summary,
                    'scores': scores
                }
                
#                 print(f"🔍 Strategy: {strategy}")
#                 print(f"📝 Summary: {generated_summary[:150]}...")
                
                if ROUGE_AVAILABLE:
                    pass
#                     print(f"📊 ROUGE Scores:")
                    for metric, score in scores.items():
                        pass
#                         print(f"   {metric}: P={score.precision:.3f}, R={score.recall:.3f}, F1={score.fmeasure:.3f}")
                else:
                    pass
#                     print(f"📊 Simple ROUGE Scores:")
                    for metric, score in scores.items():
                        pass
                        if isinstance(score, dict):
                            pass
#                             print(f"   {metric}: P={score['precision']:.3f}, R={score['recall']:.3f}, F1={score['fmeasure']:.3f}")
#                 print("-" * 40)
        
        return results
    
    def evaluate_multiple_cases(self, case_numbers, reference_strategy='semantic'):
        pass
        """Evaluate summarization across multiple cases"""
#         print(f"🎯 MULTI-CASE ROUGE EVALUATION")
#         print("=" * 50)
        
        all_results = {}
        avg_scores = {'semantic': [], 'tokenwise': [], 'recursive': []}
        
        for case_num in case_numbers:
            pass
#             print(f"\n📂 Evaluating Case {case_num}...")
            results = self.compare_chunking_strategies(case_num, reference_strategy)
            if results:
                pass
                all_results[case_num] = results
                
                # Collect scores for averaging
                for strategy, data in results.items():
                    pass
                    if strategy in avg_scores:
                        pass
                        if ROUGE_AVAILABLE:
                            pass
                            avg_scores[strategy].append(data['scores']['rouge1'].fmeasure)
                        else:
                            pass
                            avg_scores[strategy].append(data['scores']['rouge1']['fmeasure'])
        
        # Calculate and display average scores
#         print(f"\n📊 AVERAGE ROUGE-1 F1 SCORES:")
#         print("=" * 30)
        for strategy, scores in avg_scores.items():
            pass
            if scores:
                pass
                avg_score = sum(scores) / len(scores)
#                 print(f"{strategy.capitalize()}: {avg_score:.3f}")
        
        return all_results

# Initialize evaluator
evaluator = ROUGEEvaluator()
# print("ROUGE evaluator initialized!")

# Example evaluation functions
def evaluate_case_summary(case_number):
    pass
    """Quick evaluation of a single case"""
    return evaluator.compare_chunking_strategies(case_number)

def evaluate_batch_cases(case_list=None):
    pass
    """Evaluate multiple cases"""
    if case_list is None:
        pass
        case_list = available_cases[:3]  # First 3 cases
    return evaluator.evaluate_multiple_cases(case_list)

# print("\nEvaluation functions ready!")
# print("Usage examples:")
# print("• evaluate_case_summary('1')  # Evaluate case 1")
# print("• evaluate_batch_cases(['1', '2', '3'])  # Evaluate multiple cases")

# COMPREHENSIVE ROUGE COMPARISON DASHBOARD
# print("🚀 LEGAL DOCUMENT SUMMARIZATION - ROUGE EVALUATION DASHBOARD")
# print("="*70)

def display_comprehensive_evaluation(case_numbers=None):
    pass
    """Display comprehensive ROUGE evaluation with visualizations"""
    
    if case_numbers is None:
        pass
        case_numbers = available_cases[:5]  # First 5 cases for demo
    
#     print(f"📊 Evaluating {len(case_numbers)} cases: {', '.join(case_numbers)}")
#     print("="*50)
    
    # Store all results for comparison
    all_strategy_scores = {
        'semantic': {'rouge1': [], 'rouge2': [], 'rougeL': []},
        'tokenwise': {'rouge1': [], 'rouge2': [], 'rougeL': []},
        'recursive': {'rouge1': [], 'rouge2': [], 'rougeL': []}
    }
    
    detailed_results = {}
    
    # Evaluate each case
    for i, case_num in enumerate(case_numbers):
        pass
#         print(f"\n📂 CASE {case_num} EVALUATION:")
#         print("-"*40)
        
        # Get summaries from all strategies
        strategies = ['semantic', 'tokenwise', 'recursive']
        case_summaries = {}
        
        for strategy in strategies:
            pass
            chunks = loader.load_chunked_text(strategy, case_num)
            if chunks:
                pass
                summary = summarizer.extractive_summary(chunks, 5)
                case_summaries[strategy] = summary
        
        # Use semantic as reference (you can change this)
        if 'semantic' in case_summaries:
            pass
            reference_summary = case_summaries['semantic']
            
#             print(f"📋 Reference (Semantic): {reference_summary[:100]}...")
#             print()
            
            # Compare other strategies against semantic
            for strategy in ['tokenwise', 'recursive']:
                pass
                if strategy in case_summaries:
                    pass
                    generated_summary = case_summaries[strategy]
                    scores = evaluator.evaluate_summary(reference_summary, generated_summary)
                    
#                     print(f"🔍 {strategy.upper()} vs Semantic:")
#                     print(f"   Summary: {generated_summary[:80]}...")
                    
                    # Store scores for averaging
                    if ROUGE_AVAILABLE:
                        pass
                        all_strategy_scores[strategy]['rouge1'].append(scores['rouge1'].fmeasure)
                        all_strategy_scores[strategy]['rouge2'].append(scores['rouge2'].fmeasure)
                        all_strategy_scores[strategy]['rougeL'].append(scores['rougeL'].fmeasure)
                        
#                         print(f"   📊 ROUGE-1: F1={scores['rouge1'].fmeasure:.3f}")
#                         print(f"   📊 ROUGE-2: F1={scores['rouge2'].fmeasure:.3f}")
#                         print(f"   📊 ROUGE-L: F1={scores['rougeL'].fmeasure:.3f}")
                    else:
                        pass
                        all_strategy_scores[strategy]['rouge1'].append(scores['rouge1']['fmeasure'])
                        all_strategy_scores[strategy]['rouge2'].append(scores['rouge2']['fmeasure'])
                        all_strategy_scores[strategy]['rougeL'].append(scores['rougeL']['fmeasure'])
                        
#                         print(f"   📊 ROUGE-1: F1={scores['rouge1']['fmeasure']:.3f}")
#                         print(f"   📊 ROUGE-2: F1={scores['rouge2']['fmeasure']:.3f}")
#                         print(f"   📊 ROUGE-L: F1={scores['rougeL']['fmeasure']:.3f}")
#                     print()
                    
            detailed_results[case_num] = case_summaries
    
    # Display overall comparison
#     print("\n" + "="*70)
#     print("📊 OVERALL CHUNKING STRATEGY COMPARISON")
#     print("="*70)
    
    strategy_averages = {}
    for strategy in ['tokenwise', 'recursive']:
        pass
        if all_strategy_scores[strategy]['rouge1']:  # If we have scores
            pass
            avg_rouge1 = sum(all_strategy_scores[strategy]['rouge1']) / len(all_strategy_scores[strategy]['rouge1'])
            avg_rouge2 = sum(all_strategy_scores[strategy]['rouge2']) / len(all_strategy_scores[strategy]['rouge2'])
            avg_rougeL = sum(all_strategy_scores[strategy]['rougeL']) / len(all_strategy_scores[strategy]['rougeL'])
            
            strategy_averages[strategy] = {
                'rouge1': avg_rouge1,
                'rouge2': avg_rouge2,
                'rougeL': avg_rougeL
            }
            
#             print(f"\n🎯 {strategy.upper()} STRATEGY (vs Semantic baseline):")
#             print(f"   Average ROUGE-1: {avg_rouge1:.3f}")
#             print(f"   Average ROUGE-2: {avg_rouge2:.3f}")
#             print(f"   Average ROUGE-L: {avg_rougeL:.3f}")
            
            # Simple performance assessment
            if avg_rouge1 > 0.3:
                pass
#                 print(f"   ✅ Good performance (ROUGE-1 > 0.3)")
            elif avg_rouge1 > 0.2:
                pass
#                 print(f"   ⚠️ Moderate performance (ROUGE-1 > 0.2)")
            else:
                pass
#                 print(f"   ❌ Low performance (ROUGE-1 < 0.2)")
    
    # Best strategy recommendation
    if strategy_averages:
        pass
        best_strategy = max(strategy_averages.keys(), 
                          key=lambda x: strategy_averages[x]['rouge1'])
#         print(f"\n🏆 BEST PERFORMING STRATEGY: {best_strategy.upper()}")
#         print(f"   ROUGE-1 Score: {strategy_averages[best_strategy]['rouge1']:.3f}")
    
    return detailed_results, strategy_averages

# Visualization function
def create_rouge_comparison_chart(strategy_averages):
    pass
    """Create a visual comparison of ROUGE scores"""
    if not strategy_averages:
        pass
#         print("No data available for visualization")
        return
    
    strategies = list(strategy_averages.keys())
    rouge1_scores = [strategy_averages[s]['rouge1'] for s in strategies]
    rouge2_scores = [strategy_averages[s]['rouge2'] for s in strategies]
    rougeL_scores = [strategy_averages[s]['rougeL'] for s in strategies]
    
    # Simple text-based chart
#     print("\n📈 ROUGE SCORES COMPARISON CHART:")
#     print("-" * 50)
    
    max_score = max(max(rouge1_scores), max(rouge2_scores), max(rougeL_scores))
    
    for i, strategy in enumerate(strategies):
        pass
#         print(f"\n{strategy.upper()}:")
        
        # ROUGE-1
        bar_length = int((rouge1_scores[i] / max_score) * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
#         print(f"  ROUGE-1: {bar} {rouge1_scores[i]:.3f}")
        
        # ROUGE-2
        bar_length = int((rouge2_scores[i] / max_score) * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
#         print(f"  ROUGE-2: {bar} {rouge2_scores[i]:.3f}")
        
        # ROUGE-L
        bar_length = int((rougeL_scores[i] / max_score) * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
#         print(f"  ROUGE-L: {bar} {rougeL_scores[i]:.3f}")

# Run comprehensive evaluation
# print("🎯 Running comprehensive ROUGE evaluation...")
results, averages = display_comprehensive_evaluation(['1', '2', '3'])

# Create visual comparison
# print("\n")
create_rouge_comparison_chart(averages)

# print("\n" + "="*70)
# print("✅ ROUGE EVALUATION COMPLETE!")
# print("="*70)

# Install BLEU score package if not available
try:
    pass
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    BLEU_AVAILABLE = True
#     print("✅ BLEU scoring available")
except ImportError:
    pass
    BLEU_AVAILABLE = False
#     print("❌ BLEU scoring not available - install nltk")

# Enhanced Evaluation Class with BLEU Score
class EnhancedSummaryEvaluator:
    pass
    def __init__(self):
        pass
        self.smoothing_function = SmoothingFunction().method4 if BLEU_AVAILABLE else None
        
    def calculate_bleu_score(self, reference, candidate):
        pass
        """Calculate BLEU score between reference and candidate"""
        if not BLEU_AVAILABLE:
            pass
            return 0.0
        
        # Tokenize sentences
        reference_tokens = word_tokenize(reference.lower())
        candidate_tokens = word_tokenize(candidate.lower())
        
        # Calculate BLEU score
        try:
            pass
            bleu_score = sentence_bleu([reference_tokens], candidate_tokens, 
                                     smoothing_function=self.smoothing_function)
            return bleu_score
        except:
            pass
            return 0.0
    
    def comprehensive_evaluation(self, reference, candidate):
        pass
        """Comprehensive evaluation with both ROUGE and BLEU"""
        results = {}
        
        # ROUGE evaluation (using existing evaluator)
        rouge_scores = evaluator.evaluate_summary(reference, candidate)
        
        # BLEU evaluation
        bleu_score = self.calculate_bleu_score(reference, candidate)
        
        # Combine results
        if ROUGE_AVAILABLE:
            pass
            results['rouge1'] = rouge_scores['rouge1'].fmeasure
            results['rouge2'] = rouge_scores['rouge2'].fmeasure
            results['rougeL'] = rouge_scores['rougeL'].fmeasure
        else:
            pass
            results['rouge1'] = rouge_scores['rouge1']['fmeasure']
            results['rouge2'] = rouge_scores['rouge2']['fmeasure']
            results['rougeL'] = rouge_scores['rougeL']['fmeasure']
        
        results['bleu'] = bleu_score
        
        return results

# Initialize enhanced evaluator
enhanced_evaluator = EnhancedSummaryEvaluator()
# print("Enhanced evaluator with BLEU scoring initialized")

def interactive_case_analyzer():
    pass
    """Analyzer with saving results"""
#     print("🎯 INTERACTIVE LEGAL CASE ANALYZER")
#     print("=" * 60)
#     print(f"Available cases: {', '.join(available_cases[:20])}...")

#     case_number = input("🔹 Enter case number to analyze: ").strip()  # commented out for API mode
    if case_number not in available_cases:
        pass
#         print(f"❌ Case {case_number} not found!")
        return None

#     print(f"\n🔍 Analyzing Case {case_number}...")

    strategies = ['semantic', 'tokenwise', 'recursive']
    summaries = {}
    for strategy in strategies:
        pass
        chunks = loader.load_chunked_text(strategy, case_number)
        if chunks:
            pass
            summaries[strategy] = summarizer.extractive_summary(chunks, 3)

    if not summaries:
        pass
#         print("❌ Could not generate summaries")
        return None

    result = {
        'case_number': case_number,
        'summaries': summaries
    }

    # Save JSON
    json_filename = f"case_{case_number}_analysis.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        pass
        json.dump(result, f, indent=2, ensure_ascii=False)
#     print(f"✅ Analysis JSON saved as {json_filename}")

    # Save PDF
    pdf_filename = f"case_{case_number}_analysis.pdf"
    combined_summary = "\n\n".join([f"{k.upper()}:\n{v}" for k, v in summaries.items()])
    save_to_pdf(pdf_filename, case_number, combined_summary)

    return result

def quick_case_comparison(case_numbers, chunking_strategy='semantic'):
    pass
    """Quick comparison of multiple cases with summary evaluation"""
    
    if not case_numbers:
        pass
#         case_numbers = input("Enter case numbers separated by commas (e.g., 1,2,3): ").split(',')  # commented out for API mode
        case_numbers = [num.strip() for num in case_numbers]
    
#     print(f"🔄 QUICK COMPARISON: {len(case_numbers)} cases")
#     print("=" * 60)
    
    results = {}
    all_summaries = []
    
    for case_num in case_numbers:
        pass
        if case_num in available_cases:
            pass
#             print(f"📂 Processing Case {case_num}...")
            
            # Get summary
            chunks = loader.load_chunked_text(chunking_strategy, case_num)
            if chunks:
                pass
                summary = summarizer.extractive_summary(chunks, 2)  # 2 sentences
                results[case_num] = {
                    'summary': summary,
                    'word_count': len(word_tokenize(' '.join(chunks))),
                    'chunk_count': len(chunks)
                }
                all_summaries.append(summary)
                
#                 print(f"   ✅ Summary: {summary[:80]}...")
#                 print(f"   📊 Words: {results[case_num]['word_count']:,}")
#                 print(f"   📊 Chunks: {results[case_num]['chunk_count']}")
#                 print()
        else:
            pass
#             print(f"   ❌ Case {case_num} not found")
    
    # Cross-comparison using BLEU scores
    if len(all_summaries) > 1:
        pass
#         print("🔄 Cross-Comparison Analysis (BLEU Scores):")
#         print("-" * 40)
        
        for i, case1 in enumerate(results.keys()):
            pass
            for j, case2 in enumerate(results.keys()):
                pass
                if i < j:  # Avoid duplicate comparisons
                    pass
                    summary1 = results[case1]['summary']
                    summary2 = results[case2]['summary']
                    
                    bleu_score = enhanced_evaluator.calculate_bleu_score(summary1, summary2)
                    
                    similarity_level = "High" if bleu_score > 0.3 else "Medium" if bleu_score > 0.1 else "Low"
                    
#                     print(f"   Case {case1} vs Case {case2}: BLEU = {bleu_score:.3f} ({similarity_level} similarity)")
    
    return results

# print("Quick comparison tool ready! ⚡")

# Run the interactive case analyzer
# print("🎯 Starting Interactive Case Analyzer...")
# print("Note: After running, you'll be prompted to enter a case number")
# print()

# Example usage - uncomment the line below to run
# result = interactive_case_analyzer()

# Or run with a specific case (change the number as needed)
# result = interactive_case_analyzer()

# For demonstration, let's analyze a specific case
demo_case = "10"  # Change this to any available case number
# print(f"🔍 Demo Analysis for Case {demo_case}:")

# Load and display case info
metadata = loader.load_metadata(demo_case)
if metadata:
    pass
#     print(f"📋 Case Info: {metadata[:150]}...")

# Get summaries from different strategies
strategies = ['semantic', 'tokenwise', 'recursive']
demo_summaries = {}

for strategy in strategies:
    pass
    chunks = loader.load_chunked_text(strategy, demo_case)
    if chunks:
        pass
        summary = summarizer.extractive_summary(chunks, 2)
        demo_summaries[strategy] = summary
#         print(f"\n{strategy.capitalize()}: {summary[:100]}...")

# Quick evaluation
if len(demo_summaries) >= 2:
    pass
#     print(f"\n📊 Quick ROUGE & BLEU Evaluation:")
    
    if 'semantic' in demo_summaries and 'tokenwise' in demo_summaries:
        pass
        scores = enhanced_evaluator.comprehensive_evaluation(
            demo_summaries['semantic'], 
            demo_summaries['tokenwise']
        )
        
#         print(f"TokenWise vs Semantic:")
#         print(f"  ROUGE-1: {scores['rouge1']:.3f}")
#         print(f"  ROUGE-L: {scores['rougeL']:.3f}")
#         print(f"  BLEU: {scores['bleu']:.3f}")

# print("\n✅ Demo complete! Use interactive_case_analyzer() for full analysis")






import json
import re
from datetime import datetime
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import PyPDF2

# --- Entity Extractor ---
class LegalEntityExtractor:
    pass
    def __init__(self):
        pass
        self.act_patterns = [
            r'(\w+\s+Act,?\s+\d{4})',
            r'(Indian\s+\w+\s+Act)',
            r'(Code\s+of\s+\w+\s+Procedure)'
        ]
        self.section_patterns = [
            r'Section\s+\d+[A-Z]?',
            r'Article\s+\d+[A-Z]?',
            r'Rule\s+\d+[A-Z]?'
        ]
        self.citation_patterns = [
            r'AIR\s+\d{4}\s+SC\s+\d+',
            r'\d{4}\s+SCR\s*\([^\)]*\)\s*\d+'
        ]
        self.judge_patterns = [
            r'Justice\s+[A-Z][a-zA-Z]+',
            r'Hon.?ble\s+Mr.?\s+Justice\s+[A-Z][a-zA-Z]+'
        ]

    def extract(self, text):
        pass
        acts, sections, citations, judges = [], [], [], []

        for pattern in self.act_patterns:
            pass
            acts.extend(re.findall(pattern, text, re.IGNORECASE))
        for pattern in self.section_patterns:
            pass
            sections.extend(re.findall(pattern, text, re.IGNORECASE))
        for pattern in self.citation_patterns:
            pass
            citations.extend(re.findall(pattern, text))
        for pattern in self.judge_patterns:
            pass
            judges.extend(re.findall(pattern, text))

        return {
            "acts": list(set(acts)),
            "sections": list(set(sections)),
            "citations": list(set(citations)),
            "judges": list(set(judges))
        }

# --- Summarization ---
def simple_summarize(text, num_sentences=5):
    pass
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        pass
        return " ".join(sentences)
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(sentences)
    scores = np.array(tfidf_matrix.sum(axis=1)).ravel()
    top_indices = scores.argsort()[-num_sentences:][::-1]
    top_sentences = [sentences[i] for i in sorted(top_indices)]
    return " ".join(top_sentences)

# --- Load case text ---
def load_case_text(case_name: str):
    pass
    txt_path = ORIGINAL_DIR / f"{case_name}.txt"
    pdf_path = ORIGINAL_DIR / f"{case_name}.pdf"
    if txt_path.exists():
        pass
        with open(txt_path, "r", encoding="utf-8") as f:
            pass
            return f.read()
    elif pdf_path.exists():
        pass
        text = ""
        with open(pdf_path, "rb") as f:
            pass
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                pass
                page_text = page.extract_text()
                if page_text:
                    pass
                    text += page_text + "\n"
        return text
    else:
        pass
#         print("⚠️ No .txt or .pdf found. Please paste the case text below:")
#         return input("Case text: ")  # commented out for API mode

# --- Structured Summarizer ---
def structured_summarize(text):
    pass
    sentences = sent_tokenize(text)
    overview = simple_summarize(" ".join(sentences[:len(sentences)//3]), 3)
    arguments = simple_summarize(" ".join(sentences[len(sentences)//3:2*len(sentences)//3]), 3)
    decision = simple_summarize(" ".join(sentences[2*len(sentences)//3:]), 2)
    return {
        "overview": overview,
        "decision": " ".join(sent_tokenize(decision)[:3])
    }

# --- Main Summarization Function ---
# def summarize_case(case_name: str, output_format="json"):  # commented out to prevent auto-execution in API mode
    case_text = load_case_text(case_name)
    if not case_text.strip():
        pass
        return {"error": "No case text provided."}

    extractor = LegalEntityExtractor()
    entities = extractor.extract(case_text)
    structured_summary = structured_summarize(case_text)

    output = {
        "case_name": case_name,
        "judges": entities["judges"],
        "citations": entities["citations"],
        "acts": entities["acts"],
        "sections": entities["sections"],
        "summary": structured_summary,
        "timestamp": str(datetime.now())
    }

    if output_format.lower() == "json":
        pass
        out_path = f"{case_name}_summary.json"
        with open(out_path, "w", encoding="utf-8") as f:
            pass
            json.dump(output, f, indent=4, ensure_ascii=False)
#         print(f"✅ Summary saved as {out_path}")

    return output

def main():
    pass
#     case_name = input("Enter the case name (without extension): ").strip()  # commented out for API mode
#     result = summarize_case(case_name, output_format="json")  # commented out to prevent auto-execution in API mode
#     print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    pass
#     main()  # commented out to prevent auto-execution in API mode


# === Original Notebook Code Ends ===

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] if you want to restrict to frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextInput(BaseModel):
    text: str

@app.post("/summarize_text")
def summarize_text(input_data: TextInput):
    text = input_data.text
    try:
        result = main(text) if 'main' in globals() else {"summary": "main() not defined"}
    except Exception as e:
        result = {"error": str(e)}
    return result

@app.post("/summarize_pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    try:
        # 👇 Use structured_summarize to build summary
        structured_summary = structured_summarize(text)

        # 👇 Use your LegalEntityExtractor to get entities
        extractor = LegalEntityExtractor()
        entities = extractor.extract(text)

        # 👇 Build JSON result
        result = {
            "case_name": file.filename,
            "judges": entities["judges"],
            "citations": entities["citations"],
            "acts": entities["acts"],
            "sections": entities["sections"],
            "summary": structured_summary,
            "timestamp": str(datetime.now())
        }

        # ✅ Save JSON to a temporary file
        temp_path = os.path.join(tempfile.gettempdir(), f"{file.filename}_summary.json")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        # ✅ Return it as downloadable file
        return FileResponse(
            path=temp_path,
            filename=f"{file.filename}_summary.json",
            media_type="application/json"
        )

    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health_check():
    return {"status": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
