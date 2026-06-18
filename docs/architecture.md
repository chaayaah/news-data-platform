# News Data Platform Architecture

## Overview

The News Data Platform is an end-to-end Data Engineering platform inspired by enterprise content ingestion systems.

## Data Flow

XML / JSON / API / Kafka
            │
            ▼
     PySpark Ingestion
            │
            ▼
 Dynamic Mapping Engine
            │
            ▼
 Validation Framework
            │
            ▼
 Bronze Layer
            │
            ▼
 Silver Layer
            │
            ▼
 Gold Layer
            │
 ┌──────────┼───────────────┬─────────────┐
 ▼          ▼               ▼             ▼
PostgreSQL FastAPI    Dashboard      MLflow

## Principles

- Configuration-driven mapping
- Modular architecture
- Data quality first
- Bronze/Silver/Gold design
- Multiple consumers from one pipeline