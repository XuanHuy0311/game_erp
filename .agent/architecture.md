# Database Architecture: Game Management System

This document outlines the core relational database structure for the Game Management module in OpenERP.

## Entity-Relationship Diagram

```mermaid
erDiagram
    %% Core Entity
    GAME {
        Integer id PK
        String title
        Date release_date
        Float price
        Integer series_id FK
        Integer publisher_id FK
        Integer studio_id FK
    }

    %% 1-to-Many Relationships
    SERIES ||--o{ GAME : "contains"
    SERIES {
        Integer id PK
        String name
        String description
    }

    PUBLISHER ||--o{ GAME : "publishes"
    PUBLISHER {
        Integer id PK
        String name
        String country
    }

    STUDIO ||--o{ GAME : "develops"
    STUDIO {
        Integer id PK
        String name
        String headquarters
    }

    STUDIO ||--o{ MEMBER : "employs"
    MEMBER {
        Integer id PK
        String name
        String role
    }

    %% Many-to-Many Relationships (Junctions implied)
    GAME }o--o{ PLATFORM : "is available on"
    PLATFORM {
        Integer id PK
        String name
        String manufacturer
    }

    GAME }o--o{ GENRE : "is categorized as"
    GENRE {
        Integer id PK
        String name
    }