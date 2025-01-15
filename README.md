# Leukemia Subtype Scraper

A **basic scraper** designed for the isolation of all leukemia subtypes **AML** and **ALL** for downstream analysis. This tool leverages **Cellosaurus** for rapid searching of all potential synonyms and misspellings of common AML/ALL cell lines, enabling the isolation of pertinent samples and cell lines.

## Features
- **Implements Cellosaurus**: Facilitates rapid identification of synonyms/misspellings.
- **Targeted Isolation**: Filters and isolates relevant AML/ALL samples and cell lines.

## File Breakdown
### 1. `drivers_and_data`
Contains:
- **Geckodriver**: For web scraping automation.
- **Cell line information**: Metadata and references for leukemia cell lines.

### 2. Conda Environment
- **Environment file**: `encode_scraper.yml`
- To activate:  
  ```bash
  conda env create -f encode_scraper.yml
  conda activate encode_scraper
### 3. Synonym Scraper
- **Script**: `synonym_parser_framework.py`
- **Purpose**: Scrapes and identifies comprehensive synonyms for leukemia cell lines.

### 4. Comprehensive Profile
- **Notebook**: `scraper.ipynb`
- **Details**: Provides a complete overview of leukemia cell lines available in **ENCODE**.
