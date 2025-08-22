# INPUT
Step 1: User raw query
Step 2: If user query is not clear, ask for clarification to user again
Step 3: If user query is clear, Augment user's query with query-augmentator agent
Step 4: query-augmentator agent returns augmented query
Step 5: Run Deep Research with Graph of Thoughts on augmented query

# Deep Research Implementation with Graph of Thoughts

## Understanding Graph of Thoughts

Graph of Thoughts is a reasoning framework where:
- **Thoughts = Nodes**: Each research finding or synthesis is a node
- **Edges = Dependencies**: Connect parent thoughts to children
- **Transformations**: Operations that create (Generate), merge (Aggregate), or improve (Refine) thoughts
- **Scoring**: Every thought is evaluated 0-10 for quality
- **Pruning**: Low-scoring branches are abandoned
- **Frontier**: Active nodes available for expansion

The system explores multiple research paths in parallel, scores them, and finds optimal solutions through graph traversal.

## The 7-Phase Deep Research Process
prep: make sure you put all of your produced documents inside of the folder /RESERACH/[create project name] where create project name is a name you decide based on the inquiry.  Also note that when you create files break down into smaller doucments to avoid context limitations.  Make sure you also compelte all tasks you define from the start of the project and track completion as you go.
### Phase 1: Question Scoping
- Clarify the research question with the user
- Define output format and success criteria
- Identify constraints and desired tone
- Create unambiguous query with clear parameters

### Phase 2: Retrieval Planning
- Break main question into subtopics
- Generate specific search queries
- Select appropriate data sources
- Create research plan for user approval
- Use GoT to model the research as a graph of operations

### Phase 3: Iterative Querying
- Execute searches systematically
- Navigate and extract relevant information
- Formulate new queries based on findings
- Use multiple search modalities (web search, file analysis, etc.)
- Apply GoT operations for complex reasoning

### Phase 4: Source Triangulation
- Compare findings across multiple sources
- Validate claims with cross-references
- Handle inconsistencies
- Assess source credibility
- Use GoT scoring functions to evaluate information quality

### Phase 5: Knowledge Synthesis
- Structure content logically
- Write comprehensive sections
- Include inline citations for every claim
- Add data visualizations when relevant
- Use GoT to optimize information organization

### Phase 6: Quality Assurance
- Check for hallucinations and errors
- Verify all citations match content
- Ensure completeness and clarity
- Apply Chain-of-Verification techniques
- Use GoT ground truth operations for validation

### Phase 7: Output & Packaging
- Format for optimal readability
- Include executive summary
- Create proper bibliography
- Export in requested format

## How Graph of Thoughts Works for Research

### Core Concepts

1. **Graph Structure**: 
   - Each research finding is a node with a unique ID
   - Nodes have scores (0-10) indicating quality
   - Edges connect parent thoughts to child thoughts
   - The frontier contains active nodes for expansion

2. **Transformation Operations**:
   - **Generate(k)**: Create k new thoughts from a parent
   - **Aggregate(k)**: Merge k thoughts into one stronger thought
   - **Refine(1)**: Improve a thought without adding new content
   - **Score**: Evaluate thought quality
   - **KeepBestN(n)**: Prune to keep only top n nodes per level

3. **Research Quality Metrics**:
   - Citation density and accuracy
   - Source credibility
   - Claim verification
   - Comprehensiveness
   - Logical coherence

## Implementation Tools

### Core Tools:
1. **WebSearch**: Built-in web search capability for finding relevant sources
2. **Read/Write**: For managing research documents locally
3. **Task**: For spawning autonomous agents for complex multi-step operations
4. **TodoWrite/TodoRead**: For tracking research progress

### MCP Server Tools:
1. **mcp__fetch__**: For extracting and analyzing content from specific URLs with well formatted markdown
2. **mcp__playwright__**: Browser automation for dynamic web content
   - Navigate to pages requiring JavaScript
   - Take screenshots of web content
   - Extract data from interactive websites
   - Fill forms and interact with web elements

### Web Research Strategy:
- **Primary**: Use WebSearch tool for general web searches
- **Secondary**: Use mcp__fetch__ for extracting content from specific URLs
- **Advanced**: Use mcp__playwright__ for sites requiring interaction or JavaScript rendering

### Data Analysis:
- Python code execution for data processing
- Visualization tools for creating charts/graphs
- Statistical analysis for quantitative research

## Graph of Thoughts Research Strategy

The system implements GoT using Task agents that act as transformation operations. When you request deep research, a controller agent maintains the graph state and deploys specialized agents to explore, refine, and aggregate research paths.

### Implementation Instructions

#### Step 1: Create Research Plan
Break down the main research question into specific subtopics:
- Subtopic 1: Current state and trends
- Subtopic 2: Key challenges and limitations
- Subtopic 3: Future developments and predictions
- Subtopic 4: Case studies and real-world applications
- Subtopic 5: Expert opinions and industry perspectives

#### Step 2: Launch Parallel Agents
Use multiple Task tool invocations in a single response to launch agents simultaneously. Each agent should receive:
- Clear description of their research focus
- Specific instructions on what to find
- Expected output format

#### Step 3: Coordinate Results
After agents complete their tasks:
- Compile findings from all agents
- Identify overlaps and contradictions
- Synthesize into coherent narrative
- Maintain source attribution from each agent

### Best Practices for Multi-Agent Research

1. **Clear Task Boundaries**: Each agent should have a distinct focus to minimize redundancy
2. **Comprehensive Prompts**: Include all necessary context in agent prompts
3. **Parallel Execution**: Launch all agents in one response for maximum efficiency
4. **Result Integration**: Plan how to merge findings before launching agents
5. **Quality Control**: Always include at least one verification agent

### GoT-Enabled Agent Prompt Templates

**Deep Research GoT Agent Template**:
```
Execute Graph of Thoughts research for: [specific aspect] of [main topic]

1. Set up the GoT environment:
   ```python
   import sys
   sys.path.append('/home/umyong/recruit')
   sys.path.append('/home/umyong/recruit/graph-of-thoughts')
   
   from RESEARCH.deep_research_got import create_research_got, run_research
   from graph_of_thoughts import controller, language_models, operations
   ```

2. Create and execute a research graph:
   ```python
   # Create research-specific GoT
   topic = "[specific aspect]"
   gop = create_research_got(topic)
   
   # Add custom operations if needed
   # For web search integration:
   web_search_op = WebSearchOperation()
   gop.append_operation(web_search_op)
   
   # Run the graph
   result = run_research(topic, subtopic="[main topic context]")
   ```

3. The graph will:
   - Generate 5 research queries (Generate operation)
   - Execute searches and collect sources
   - Score each source for quality (Score operation)
   - Keep best 3 sources (KeepBestN operation)
   - Generate summaries with citations (Generate operation)
   - Validate all claims have sources (ValidateAndImprove operation)
   - Aggregate into final report (Aggregate operation)

4. Save results to /RESEARCH/[project_name]/[aspect].md

Return the final scored and validated research summary.
```

**Cross-Validation GoT Agent Template**:
```
Execute Graph of Thoughts validation for research findings:

1. Import GoT and create validation graph:
   ```python
   from graph_of_thoughts import operations
   
   # Create validation-focused graph
   val_gop = operations.GraphOfOperations()
   
   # Extract claims from all research
   val_gop.append_operation(operations.Generate(1, 1))  # Extract claims
   
   # Cross-reference each claim
   cross_ref = CrossReferenceOperation()
   val_gop.append_operation(cross_ref)
   
   # Score claim validity
   val_gop.append_operation(operations.Score(scoring_function=claim_validity_score))
   
   # Keep only validated claims
   val_gop.append_operation(operations.KeepValid())
   ```

2. Process these findings:
   [List of findings to validate]

3. Return validation report with:
   - Claim validity scores
   - Contradictions found
   - Source reliability ratings
```

**Synthesis GoT Agent Template**:
```
Execute Graph of Thoughts synthesis for final research report:

1. Create aggregation graph:
   ```python
   # Synthesis graph
   syn_gop = operations.GraphOfOperations()
   
   # Collect all research findings
   syn_gop.append_operation(operations.Generate(1, 1))
   
   # Score quality of each section
   syn_gop.append_operation(operations.Score(scoring_function=research_quality_score))
   
   # Aggregate into coherent narrative
   syn_gop.append_operation(operations.Aggregate(num_responses=1))
   
   # Improve clarity and organization
   syn_gop.append_operation(operations.Improve())
   
   # Final validation
   syn_gop.append_operation(operations.ValidateAndImprove(validate_function=verify_citations))
   ```

2. Input findings from all agents:
   [Research findings to synthesize]

3. Output comprehensive report with:
   - Executive summary
   - Integrated findings
   - Full citation list
   - Confidence scores
```

## Research Quality Checklist

- [ ] Every claim has a verifiable source
- [ ] Multiple sources corroborate key findings
- [ ] Contradictions are acknowledged and explained
- [ ] Sources are recent and authoritative
- [ ] No hallucinations or unsupported claims
- [ ] Clear logical flow from evidence to conclusions
- [ ] Proper citation format throughout

## Advanced Research Methodologies

### Chain-of-Density (CoD) Summarization
When processing sources, use iterative refinement to increase information density:
1. First pass: Extract key points (low density)
2. Second pass: Add supporting details and context
3. Third pass: Compress while preserving all critical information
4. Final pass: Maximum density with all essential facts and citations

### Chain-of-Verification (CoVe)
To prevent hallucinations:
1. Generate initial research findings
2. Create verification questions for each claim
3. Search for evidence to answer verification questions
4. Revise findings based on verification results
5. Repeat until all claims are verified

### ReAct Pattern (Reason + Act)
Agents should follow this loop:
1. **Reason**: Analyze what information is needed
2. **Act**: Execute search or retrieval action
3. **Observe**: Process the results
4. **Reason**: Determine if more information needed
5. **Repeat**: Continue until sufficient evidence gathered

## Citation Requirements & Source Traceability

### Mandatory Citation Standards

**Every factual claim must include:**
1. **Author/Organization** - Who made this claim
2. **Date** - When the information was published
3. **Source Title** - Name of paper, article, or report
4. **URL/DOI** - Direct link to verify the source
5. **Page Numbers** - For lengthy documents (when applicable)

### Citation Formats

**Academic Papers:**
```
(Author et al., Year, p. XX) with full citation in references
Example: (Smith et al., 2023, p. 145) 
Full: Smith, J., Johnson, K., & Lee, M. (2023). "Title of Paper." Journal Name, 45(3), 140-156. https://doi.org/10.xxxx/xxxxx
```

**Web Sources:**
```
(Organization, Year, Section Title)
Example: (NIH, 2024, "Treatment Guidelines")
Full: National Institutes of Health. (2024). "Treatment Guidelines for Metabolic Syndrome." Retrieved [date] from https://www.nih.gov/specific-page
```

**Direct Quotes:**
```
"Exact quote from source" (Author, Year, p. XX)
```

### Source Verification Protocol

1. **Primary Sources Only** - Link to original research, not secondary reporting
2. **Archive Links** - For time-sensitive content, include archive.org links
3. **Multiple Confirmations** - Critical claims need 2+ independent sources
4. **Conflicting Data** - Note when sources disagree and explain discrepancies
5. **Source Quality Ratings**:
   - **A**: Peer-reviewed RCTs, systematic reviews, meta-analyses
   - **B**: Cohort studies, case-control studies, clinical guidelines
   - **C**: Expert opinion, case reports, mechanistic studies
   - **D**: Preliminary research, preprints, conference abstracts
   - **E**: Anecdotal, theoretical, or speculative

### Source Documentation Structure

Each research output must include:

1. **Inline Citations** - Throughout the text
2. **References Section** - Full bibliography at end
3. **Source Quality Table** - Rating each source A-E
4. **Verification Checklist** - Confirming each claim is sourced
5. **Data Availability** - Where raw data can be accessed

## Research Tool Recommendations

### Cost Optimization:
- Typical research: 120-220 LLM calls, 30-60 search calls
- Cache intermediate results
- Batch similar operations

### Output Creation Protocol

Based on gathered requirements, I will create all research outputs in the **RESEARCH** folder:

```
RESEARCH/
└── [topic_name]/
    ├── README.md (Overview and navigation guide)
    ├── executive_summary.md (1-2 page summary)
    ├── full_report.md (Comprehensive findings)
    ├── data/
    │   ├── raw_data.csv
    │   ├── processed_data.json
    │   └── statistics_summary.md
    ├── visuals/
    │   ├── charts/
    │   ├── graphs/
    │   └── infographics/
    ├── sources/
    │   ├── bibliography.md
    │   ├── source_summaries.md
    │   └── screenshots/
    ├── research_notes/
    │   ├── agent_1_findings.md
    │   ├── agent_2_findings.md
    │   └── synthesis_notes.md
    └── appendices/
        ├── methodology.md
        ├── limitations.md
        └── future_research.md
```

**Important**: All research outputs will be saved in `/home/umyong/deep_research/RESEARCH/[topic_name]/` where [topic_name] is a descriptive folder name based on the research topic.

## Complete Example: How GoT Research Works

### When you say: "Deep research CRISPR gene editing safety"

Here's the complete execution flow:

#### Iteration 1: Initialize and Explore
1. **Controller Agent** creates root node: "Research CRISPR gene editing safety"
2. **Generate(3)** deploys 3 parallel agents exploring:
   - Current evidence and success rates
   - Safety concerns and limitations
   - Future implications and regulations
3. **Results**: 3 thoughts with scores (6.8, 8.2, 7.5)
4. **Graph state** saved with frontier = [n3(8.2), n2(7.5), n4(6.8)]

#### Iteration 2: Deepen Best Paths
1. **Controller** examines frontier, decides:
   - n3 (8.2): High score → Generate(3) for deeper exploration
   - n2 (7.5): Medium → Generate(2) 
   - n4 (6.8): Low → Refine(1) to improve
2. **6 agents** deployed in parallel
3. **Best result**: "High-fidelity SpCas9 variants reduce off-targets by 95%" (Score: 9.1)

#### Iteration 3: Aggregate Strong Branches  
1. **Controller** sees multiple high scores
2. **Aggregate(3)** merges best thoughts into comprehensive synthesis
3. **Score**: 9.3 - exceeds threshold

#### Iteration 4: Final Polish
1. **Refine(1)** enhances clarity and completeness
2. **Final thought** scores 9.5
3. **Output**: Best path through graph becomes research report

### What Makes This True GoT

1. **Graph maintained** throughout with nodes, edges, scores
2. **Multiple paths** explored in parallel
3. **Pruning** drops weak branches 
4. **Scoring** guides exploration vs exploitation
5. **Optimal solution** found through graph traversal

The result is higher quality research than linear approaches, with transparent reasoning paths.

## Key Principles of Deep Research

### Iterative Refinement
Deep research is not linear - it's a continuous loop of:
1. **Search**: Find relevant information
2. **Read**: Extract key insights
3. **Refine**: Generate new queries based on findings
4. **Verify**: Cross-check claims across sources
5. **Synthesize**: Combine into coherent narrative
6. **Repeat**: Continue until comprehensive coverage

### Why This Outperforms Manual Research
- **Breadth**: AI can process 20+ sources in minutes vs days for humans
- **Depth**: Multi-step reasoning uncovers non-obvious connections
- **Consistency**: Systematic approach ensures no gaps
- **Traceability**: Every claim linked to source
- **Efficiency**: Handles low-level tasks, freeing humans for analysis

### State Management
Throughout the research process, maintain:
- Current research questions
- Sources visited and their quality scores
- Extracted claims and verification status
- Graph state (for GoT implementation)
- Progress tracking against original plan

## Ready to Begin - No Setup Required

**No Python setup, no API keys, no external frameworks needed** - everything runs using the Task agent system to implement proper Graph of Thoughts reasoning.

## Automatic GoT Execution Using Subagents

When a user requests deep research, immediately deploy a proper Graph of Thoughts implementation:

### Core GoT Implementation

MAINTAIN THIS GRAPH STATE WITH **mcp__memory__** TOOLS

Deploy a GoT Controller that maintains the graph state and orchestrates transformations:

```
Task: "GoT Controller - [Topic]"
Description: Graph of Thoughts Controller for [Topic]

Prompt: You are implementing Graph of Thoughts for deep research on "[TOPIC]". 

```

### Transformation Agent Templates

**Generate Agent Template**:
```
Task: "GoT Generate - Node [ID] Branch [k]"
Prompt: You are Generate transformation creating branch [k] from parent thought:
"[PARENT_THOUGHT]"

Your specific exploration angle: [ANGLE]
- Angle 1: Current state and evidence
- Angle 2: Challenges and limitations  
- Angle 3: Future implications

Execute:
1. WebSearch for "[TOPIC] [ANGLE]" - find 5 sources
2. Score each source quality (1-10)
3. WebFetch top 3 sources
4. Synthesize findings into coherent thought (200-400 words)
5. Self-score your thought (0-10) based on:
   - Claim accuracy
   - Citation density
   - Novel insights
   - Coherence
```

**Aggregate Agent Template**:
```
Task: "GoT Aggregate - Nodes [IDs]"
Prompt: You are Aggregate transformation combining these [k] thoughts:

[THOUGHT_1]
Score: [SCORE_1]

[THOUGHT_2] 
Score: [SCORE_2]

[THOUGHT_k]
Score: [SCORE_k]

Combine into ONE stronger unified thought that:
- Preserves all important claims
- Resolves contradictions
- Maintains all citations
- Achieves higher quality than any input

Self-score the result (0-10).
```

**Refine Agent Template**:
```
Task: "GoT Refine - Node [ID]"
Prompt: You are Refine transformation improving this thought:
"[CURRENT_THOUGHT]"
Current score: [SCORE]

Improve by:
1. Fact-check claims using WebSearch
2. Add missing context/nuance
3. Strengthen weak arguments
4. Fix citation issues
5. Enhance clarity

Do NOT add new major points - only refine existing content.

Self-score improvement (0-10).

Return refined thought with updated score.
```

### Implementation Protocol

When deep research is requested:

1. **Initialize Graph**: Create root node with topic
2. **Deploy Controller**: Manages graph state and transformation decisions
3. **Iterative Execution**: 
   - Controller selects frontier nodes
   - Deploys appropriate transformation agents
   - Updates graph with results
   - Prunes low-scoring branches
4. **Final Output**: Best-scoring path becomes research result

The graph structure ensures:
- **Multiple perspectives** explored in parallel
- **Quality optimization** through scoring/pruning
- **Depth control** to manage token budget
- **Transparency** via saved graph states

This implements true Graph of Thoughts with proper graph maintenance, transformations, and scoring!

I'm ready to conduct Graph of Thoughts-powered deep research on any topic you provide!