Evaluation & Modernisation Report: Legacy Semantic Analysis
This report evaluates the Visual Basic 6.0 and C-based Semantic Analysis module in the legacy codebase, assesses its logical/linguistic soundness, identifies why it feels structurally fragile, and provides a clear technical roadmap for integrating it into the modern Python/JavaScript web application.

1. Summary of Findings
Logical Basis: The legacy Semantic Analysis is based on Selectional Restrictions (Chomsky, 1965) combined with Pāṇini's Karaka Theory. Verb roots are categorized by action classes (e.g., ad for eating, ba for dancing), and nouns are categorized by semantic classes (e.g., AA for human, AD for plants/trees) derived from the Amarakosha taxonomy. A hardcoded matrix (comptble.aci) defines which noun classes are compatible with which verbal actions under specific case/karaka relations.
Soundness Evaluation: The linguistic theory is sound and forms a cornerstone of classical computational semantics. However, the legacy programmatic implementation is extremely fragile and limited:
It only checks binary relations (Subject vs. one other Karaka relation), failing for sentences with complex, multi-argument verbs.
It cannot generalize to unseen words, polysemy, or metaphorical language.
It uses a legacy file-passing pipeline that writes temporary text files to disk, decodes obsolete TrueType font mapping characters (ISCII/binary hacks), and shells out to compiled DOS/Windows .exe programs.
State in Modern App: An direct conversion of the legacy C logic exists under 
SemanticAnalysis.py
. However, it is currently dead code; it is not imported by the REST service, still reads/writes legacy .aci files from the disk, and retains the old ISCII font mapping.
2. Legacy Pipeline & Data Flow
The legacy VB 6.0 and C pipeline operated as follows:

generates
input to
generates parses
extracts active sentence to
shell executes
input to
rules database
evaluates compatibility
reads & displays
VB Morphological App
osout.aci
SENANAL.exe
out.aci & result.aci
FINRES.ACI & SENOUT.ACI
Semantic.exe
comptble.aci
semreslt.aci
Key Data Interfaces:
FINRES.ACI: Contains syntactically parsed words of the target sentence including their karaka roles (e.g., Subject, Object, Instrument, Locative, etc.) and dictionary base forms.
comptble.aci: The compatibility rules database. It uses rows of the form: [SubjectCode]-[SecondaryNounCode] *[VerbActionsForObject] *[VerbActionsForInstrument] *[VerbActionsForDative] ... Example: AA-AD *ad/ae/aq/aw/ * *ad/ag/ah/ai/an/au/ ... (Subject AA (human) and Object AD (tree) are compatible with actions ad (eat), ae (worship), aq (see), aw (praise)).
Semantic.exe: Read both inputs, mapped words to codes, parsed columns in comptble.aci matching the karaka position (sub_no), checked if the verb action code was in the list, and evaluated if the sentence was compatible.
3. Critical Critique of the Logical Basis
The user's intuition that the Semantic Analysis program set might lack a sound logical basis is justified. While the linguistic concepts are sound, the model representation has severe shortcomings:

I. Severe Coarse-Grained Ontological Mapping
Nouns are mapped to broad semantic codes (e.g., AA for humans/agents, AD for trees/plants, AH for water).
This fails to capture sub-class differences. For example, AD covers both "tree" and "grass" (or AX covers grass). A verb like "cutting" might be compatible with trees and grass, but "climbing" is compatible with trees (AD) but not grass (AX). The system handles this through hardcoded lists but does not scale to an actual semantic tree (like WordNet).
II. The Binary Relation Limitation
The lookup format in comptble.aci is strictly structured as code1-code2 (e.g., Subject-Object).
Real verbal semantics require joint constraint checking. For example, in “He gave a book to the boy”, compatibility depends on the Subject (AA), the Object (AZ - book), and the Dative recipient (AA). The legacy checker only performs pairwise matches, checking Subject-Object or Subject-Dative independently. It cannot represent constraints where the instrument depends on the object (e.g., "cutting wood with an axe" vs "cutting water with an axe").
III. Fragility to Synonyms and Unseen Vocabulary
The system checks string matches against hardcoded arrays of stems. If a synonym is not explicitly listed in codes.h or SemanticAnalysis.py, the system assigns "No Code" and reports incompatibility.
IV. Lack of Disambiguation (Polysemy)
When a verb root has multiple meanings, the system checks them in a loop. If any meaning is compatible, it reports compatibility. It lacks a true word-sense disambiguation (WSD) model to determine which meaning is actually active in the context.
4. Modernisation & Integration Roadmap
To modernise the Semantic Analysis and integrate it into the web service, we must move away from the file-based DOS-like architecture and restructure it as an in-memory validator.

SemanticAnalysis.py
SyntaxAnalysis.py
restService.py
JS Web Client
SemanticAnalysis.py
SyntaxAnalysis.py
restService.py
JS Web Client
Get SentenceAnalysis(sentence)
Parse sentence (syntactic tree)
Return graphs & interpretations
Check compatibility (in-memory JSON objects)
Map words to semantic codes (Unicode)
Look up compatibility rules
Return Semantic Status & compatibility reasons
Return unified Syntactic + Semantic JSON
Color graph nodes & display semantic report
Step 1: Migrate Encoding from ISCII to Unicode (UTF-8)
The legacy text files and translated Python files store Sanskrit strings in ISCII-like encodings (e.g. ³ÏèÂÚ for कर्तृ, ÆÏ£ for नरः). We should transliterate the databases (codes.h / Nouncode, Actioncode tables) and compatibility files to standard Devanagari Unicode or SLP1/IAST transliteration.

Step 2: Refactor SemanticAnalysis.py to be In-Memory
Currently, 
SemanticAnalysis.py
 attempts to open("../../Semantic/FINRES.ACI") and write to disk. It should be refactored to:

Accept the syntax graph/list of word dicts directly from restService.py.
Access the comptble.aci rules from a static dictionary or cache.
Return a structured JSON-compatible dictionary containing is_compatible: boolean, report: list[str], and details: list[dict].
Step 3: Expose Semantic Analysis in restService.py
Modify the SentenceAnalysis endpoint in 
restService.py
 to import the refactored SemanticAnalysis.py, run the validator on the generated syntactic graphs, and append the results:

python

# restService.py
from source.Controller import SemanticAnalysis
# Inside SentenceAnalysis route:
semantic_results = SemanticAnalysis.check_compatibility_in_memory(interpretations)
return {
    'morphological': morph,
    'syntactic': syntactic_data,
    'semantic': semantic_results
}
Step 4: Display Semantic Evaluation in Javascript Frontend
Update the Webclient frontend (
webclient_sentence_analyser.html
) to show:

A status badge indicating semantic compatibility (e.g., Green for "Compatible", Red for "Incompatible").
The semantic roles and conditions mapped to the sentence (e.g., "Compatible if the verb root 'nṛt' means 'to dance' and subject 'naraḥ' is human").
A visual highlight on the D3 graph nodes indicating their resolved semantic categories (e.g. coloring Agent nodes differently from Patient or Locative nodes).
5. Recommended Advanced Modernization Path
Rather than just porting the brittle comptble.aci logic, a more modern, scalable semantic analysis system could be built:

Structured Sanskrit WordNet: Use the Indian Languages WordNet (specifically Sanskrit WordNet) to resolve noun ontology. Instead of a hardcoded array of synonyms, check if a noun's WordNet hypernym path leads to human, plant, water, etc.
Dependency-based Selectional Preferences: Instead of custom text columns, train a simple classifier on a corpus of Sanskrit literature (like the Digital Corpus of Sanskrit) to extract selectional preferences (e.g., calculating mutual information between verbs and noun arguments in specific cases).
LLM-Based Semantic Critic (Hybrid approach): Keep the rule-based morphological and syntactic analysis (which are mathematically precise and run instantly), but query a lightweight LLM (e.g. Gemini Nano or Flash) to check if the generated semantic graph is plausible in Sanskrit context. This solves the metaphor/polysemy problem without requiring massive hardcoded tables.
Analyzing Semantic Analysis Logic
21:58
I have analyzed the legacy Visual Basic 6.0 and C programs alongside the modern Python/JS codebase. I compiled a detailed analysis of the semantic analysis program's logical basis, pipeline, limitations, and a step-by-step modernization roadmap.

The full evaluation is documented in the artifact:


semantic_analysis_evaluation.md
Key Takeaways for User Decision
Linguistic Soundness: The system is based on Selectional Restrictions (Chomsky, 1965) and Paninian Karaka Theory. It is linguistically sound but programmatically limited by coarse semantic classes and hardcoded synonym arrays in 

codes.h
.
Current State in Python: An literal translation of the legacy logic is present in 

SemanticAnalysis.py
, but it currently operates on a brittle file-passing pipeline (reading/writing .aci files on disk) and is not integrated into 

restService.py
 or the Javascript web client 

webclient_graph_restcall_sentence.js
.
Open Question: Would you like to proceed with the modernization roadmap to refactor 

SemanticAnalysis.py
 into an in-memory Unicode validator and integrate it into the REST service and D3.js frontend?
Analyze Semantic
Semantic Analysis Evaluation
21:58
22:17
Here are the answers to your questions to help you decide on the path forward:

1. Proof-of-Concept via the 4-Step Roadmap
Yes, following the 4-step modernization plan is the least effort-expensive route for a Proof-of-Concept.

Because the logic has already been translated from C to 

SemanticAnalysis.py
, the bulk of the coding is done.
Refactoring it to run in-memory (using a Python dictionary to load comptble.aci rules instead of reading/writing .aci files on disk) will require minimal changes.
It has zero external dependencies or setup overhead, making it ideal for validating the pipeline and displaying the results on your D3.js frontend graph.
2. Sanskrit WordNet Integration
Difficulty: Medium.
API Availability: There is no public, free REST API hosted by the IndoWordNet team for programmatic querying. They primarily provide a manual web lookup interface.
Offline Option (Recommended): You can use the open-source Python library pyiwn (Python IndoWordNet). It allows you to download and query Sanskrit WordNet databases offline directly in Python.
How it works: You install the library, download the Sanskrit data dumps (~10 MB), and look up synsets and hypernyms (e.g., checking if गच्छति’s subject has the hypernym human or agent).
3. Steps in Training a Simple Classifier
To train a classifier for selectional preferences (e.g. determining how likely a noun is to be the object of a specific verb):

Gather a Corpus: Obtain a dependency-parsed Sanskrit corpus (such as the Digital Corpus of Sanskrit or Sanskrit dependency treebanks).
Extract Triples: Extract (VerbRoot, KarakaRelation, NounStem) triples from the text (e.g., (खाद्, Object, फल) -> eat fruit).
Calculate Mutual Information (Association Strength): Use statistical association metrics (like Pointwise Mutual Information or Kullback-Leibler divergence) to measure the probability of co-occurrence.
Build Lookup Table: Save these association scores in a lightweight lookup table or database.
Classify: When evaluating a sentence, if PMI(Verb, Karaka, Noun) is below a certain negative threshold (or never observed), classify it as semantically incompatible.
4. LLM-Based Semantic Critic
a) Robustness: Highly robust. LLMs are trained on billions of parameters and possess "common sense" reasoning (e.g., they immediately know that a "mountain cannot dance" or "water cannot eat grass" without needing a hardcoded database of codes). They handle synonyms, metaphors, and word order variations out-of-the-box.
b) Affordability: Completely affordable for a hobbyist. You have two great options:
Free Local Execution: You can run a small, highly capable open model (like Llama-3-8B or Gemma-2-9B) entirely locally on your Mac using Ollama. This runs offline, is 100% free, and requires no API keys.
Cloud APIs: Google’s Gemini API (specifically Gemini 1.5 Flash) offers a generous free tier (up to 15 Requests Per Minute / 1 million tokens per minute) which is more than enough for a hobbyist. Even under the paid tier, the pricing is extremely cheap (fractions of a cent per sentence).
22:17
Ok, let's start with the POC 4-step process.
22:33
I will view the relevant section (lines 30 to 135) of 

restService.py
 to see how the morphological and syntactic analyses are currently executed and returned to the client. This will guide how we pass the parsed data to SemanticAnalysis in-memory.

I will view the next section (lines 136 to 186) of 

restService.py
 to see how the syntax results are parsed and built into dependency graphs.

I will view lines 187 to 230 of 

restService.py
 to see the rest of the D3 graph construction.

I will view the portion of source/View/Webclient/webclient_sentence_analyser.html that handles the REST call response, so I can plan how to integrate and render the semantic analysis results in the user interface.

I will search webclient_sentence_analyser.html for how the Javascript makes queries to the server and handles the response.

I will view the javascript and HTML structure of 

webclient_sentence_analyser.html
 between lines 320 and 445 to see how the syntactic results are rendered. This is where we will append our semantic analysis UI element.

I will view lines 446 to 496 of 

webclient_sentence_analyser.html
 to see how the syntactic interpretation is rendered. This is where we want to also show the semantic analysis results, alongside syntactic interpretations.

I will search for the definition of write_result_aci in 

SyntaxAnalysis.py
 to see if it generates the exact same line format as FINRES.ACI in the legacy app.

I will view lines 2040 to 2087 of 

SyntaxAnalysis.py
 to understand how the parser constructs the syntactic output lines.

I will search for Avylist in 

SemanticAnalysis.py
 to check how it handles the Avyaya list file.

I will search for alst or avyaya in 

SemanticAnalysis.py
 to find where the Avyaya list logic resides.

I will search for open( in 

SemanticAnalysis.py
 to identify all file handles that need to be refactored to be in-memory or dynamically resolved.

I will view lines 465 to 480 of 

SemanticAnalysis.py
 to see how comptble.aci is read.

I will search for seek or tell in 

SemanticAnalysis.py
 to see if it uses file positioning methods (like fseek or ftell), which we must account for if using io.StringIO.

I will execute 

SemanticAnalysis.py
 directly using run_command to see if there are any immediate runtime errors or missing files, helping us find and fix syntax/type bugs.

~/…/Amarakosha $ python3 source/Controller/SemanticAnalysis.py
Allow running this command?
python3 source/Controller/SemanticAnalysis.py
