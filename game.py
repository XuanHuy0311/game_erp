# -*- coding: utf-8 -*-
"""
OpenERP v7 Game Management Module - Python ORM Models

This module defines the core business objects (models) for managing video game 
information, including games, publishers, studios, members, genres, platforms, 
and game series. The module uses OpenERP's legacy OSV (Object Services) ORM, 
which operates through the _name identifier and _columns dictionary pattern.

All models inherit from osv.Model, which automatically handles database table creation,
record persistence, and relationship management through OpenERP's ORM layer.
"""

from openerp.osv import fields, osv


class Game(osv.Model):
    """
    GAME MODEL - Core entity for video game information
    
    Represents a single video game title with comprehensive metadata including
    release information, genre classification, pricing, and relationships to
    publisher, developer studio, and available platforms.
    
    Relationships:
    - many2one: publisher_id, studio_id, series_id (Parent records)
    - many2many: platforms (Multiple platforms via junction table)
    
    Example: A record might be "The Witcher 3", published by CD Projekt Red,
    developed by CD Projekt Red, released in 2015, available on PC, PS4, Xbox One.
    """
    
    _name = 'game.game'  # Database table: game_game
    _columns = {
        # ===== BASIC INFORMATION FIELDS =====
        
        'name': fields.char(
            'Tên game',
            size=25,
            required=True,
            translate=True  # Allows multi-language game titles
        ),
        # Example: 'The Witcher 3', 'Elden Ring', 'Baldur\'s Gate 3'
        # Note: size=25 limits the character count; consider increasing for longer titles
        
        'description': fields.text('Mô tả'),
        # Large text field for detailed game summary and narrative
        # No size limit - appropriate for marketing descriptions
        # Example: "An open-world action RPG set in a fantasy realm..."
        
        # ===== GENRE CLASSIFICATION (Selection Field) =====
        
        'genre': fields.selection([
            # This is a fixed set of choices. Users select ONE genre per game.
            # In a production system, consider using many2many to game.genre model
            # for more flexible multi-genre assignment.
            ('action', 'Hành động'),           # Action games
            ('rpg', 'Nhập vai'),               # Role-playing games
            ('fps', 'Bắn súng'),               # First-person shooters
            ('adventure', 'Chinh phục'),       # Adventure/exploration
            ('simulation', 'Simulación'),      # Simulation games
            ('sports', 'Thể thao'),            # Sports games
            ('strategy', 'Chính lược'),        # Strategy games
            ('puzzle', 'Tìm hiểu'),            # Puzzle games
            ('educational', 'Học tập'),       # Educational games
            ('arcade', 'Arcade'),              # Arcade/retro games
            ('racing', 'Giải nhiệm'),         # Racing games
            ('fighting', 'Đấu tranh'),        # Fighting games
            ('platformer', 'Platformer'),      # 2D platformers
            ('role-playing', 'Nhập vai'),      # RPG (alternate label)
            ('shooter', 'Bắn súng'),           # Shooter (alternate label)
            ('mmo', 'MMORPG'),                 # Massively Multiplayer Online
            ('massively-multiplayer', 'MMO')   # MMO (alternate label)
        ], 'Thể loại', required=True),
        # Note: Duplicate entries (sports, simulation, etc.) should be deduplicated
        # in production. The selection field returns a single string value.
        
        # ===== RELEASE AND STATUS FIELDS =====
        
        'release_date': fields.datetime('Ngày phát hành'),
        # Datetime field storing when the game was officially released
        # Format: YYYY-MM-DD HH:MM:SS
        # Example: '2023-06-23 00:00:00' for Baldur's Gate 3
        
        'status': fields.selection([
            ('released', 'Đã phát hành'),      # Already released to public
            ('upcoming', 'Sắp phát hành'),     # Scheduled for future release
            ('cancelled', 'Đã hủy')            # Development cancelled
        ], 'Trạng thái', required=True),
        # Allows filtering games by lifecycle stage
        
        # ===== PRICING AND DETAILS =====
        
        'notes': fields.text('Chi tiết'),
        # Additional notes and specifications about the game
        # Example: "60 FPS on next-gen consoles, cross-platform save sync"
        
        'price': fields.float('Giá'),
        # Retail/store price in numerical format
        # Example: 59.99 or 29.99
        
        # ===== FOREIGN KEY RELATIONSHIPS (many2one) =====
        # many2one creates a parent-child relationship where:
        # - A Game belongs to ONE Publisher, Studio, or Series
        # - Multiple Games can belong to the same Publisher/Studio/Series
        # - In the database: stores the foreign key ID
        # - In the XML form: displays a dropdown selector
        
        'publisher_id': fields.many2one(
            'game.publisher',  # Target model
            'Nhà phát hành'    # Field label (Vietnamese: "Publisher")
        ),
        # Links to the Publisher who distributes this game
        # Example: EA Games, Activision, Ubisoft
        
        'studio_id': fields.many2one(
            'game.studio',     # Target model
            'Nhà phát triển'   # Field label (Vietnamese: "Developer Studio")
        ),
        # Links to the Studio that developed this game
        # Example: BioWare, Naughty Dog, FromSoftware
        
        'series_id': fields.many2one(
            'game.series',     # Target model
            'Series'           # Field label
        ),
        # Links to the Game Series this title belongs to
        # Example: The Witcher (series) contains The Witcher 1, 2, 3
        
        # ===== MANY-TO-MANY RELATIONSHIP =====
        # many2many creates peer-to-peer relationships where:
        # - A Game can be on MANY Platforms
        # - A Platform can host MANY Games
        # - OpenERP creates a junction table: game_platform_rel
        # - In XML form: can use widget="many2many_tags" for modern tag UI
        
        'platforms': fields.many2many(
            'game.platform',           # Target model
            'game_platform_rel',       # Junction table name (created automatically)
            'game_id',                 # Column in junction table pointing to Game
            'platform_id',             # Column in junction table pointing to Platform
            'Máy tính'                 # Field label (Vietnamese: "Platforms")
        ),
        # Example: A game might be available on PC, PlayStation 5, Xbox Series X
        # This field stores multiple platform IDs in the junction table
    }


class Publisher(osv.Model):
    """
    PUBLISHER MODEL - Manages game publishers/distributors
    
    A publisher is a company that distributes games to the market.
    One publisher can distribute multiple games (one2many relationship).
    
    Example: Electronic Arts (EA), Activision Blizzard, Ubisoft
    """
    
    _name = 'game.publisher'  # Database table: game_publisher
    _columns = {
        'name': fields.char(
            'Tên nhà phát hành',
            size=25,
            required=True  # Cannot create a publisher without a name
        ),
        # Example: 'Electronic Arts', 'CD Projekt Red', '2K Games'
        
        'country': fields.char(
            'Quốc gia',
            size=25
        ),
        # Country where the publisher is headquartered
        # Example: 'United States', 'Poland', 'Japan'
        # Note: This is an optional field (not required=True)
    }


class Studio(osv.Model):
    """
    STUDIO MODEL - Manages development studios
    
    A studio is a company that develops (creates) games.
    One studio can develop multiple games and employ multiple members.
    
    Relationships:
    - one2many: members (Reverse relationship to Member model)
      Allows viewing all employees within a studio from the studio record
    
    Example: CD Projekt Red (Poland), FromSoftware (Japan), Insomniac (USA)
    """
    
    _name = 'game.studio'  # Database table: game_studio
    _columns = {
        'name': fields.char(
            'Tên nhà phát triển',
            size=25,
            required=True
        ),
        # Example: 'Naughty Dog', 'Insomniac Games', 'Bethesda Game Studios'
        
        'headquarter': fields.char(
            'Trụ sở chính',
            size=25
        ),
        # Primary headquarters/office location
        # Example: 'Tokyo, Japan', 'Los Angeles, USA', 'Warsaw, Poland'
        
        # ===== REVERSE RELATIONSHIP (one2many) =====
        # one2many creates a virtual parent-to-children relationship:
        # - A Studio has MANY Members
        # - Each Member has ONE Studio (via the studio_id foreign key)
        # - This field is VIRTUAL - it doesn't store data in game_studio table
        # - It queries the game_member table for all records with this studio_id
        # - In XML: displayed as an embedded <tree> within a <notebook> page
        
        'members': fields.one2many(
            'game.member',     # Target model (the child model)
            'studio_id',       # Foreign key column in game_member table pointing back here
            'Nhân viên'        # Field label (Vietnamese: "Employees")
        ),
        # Example: Naughty Dog's studio record would show all its developers
        # This is read from the game_member model where studio_id matches this studio
    }


class Member(osv.Model):
    """
    MEMBER MODEL - Manages development team members
    
    Represents an employee working at a game development studio.
    Each member belongs to exactly ONE studio.
    
    Relationships:
    - many2one: studio_id (Parent relationship)
      A Member must be associated with a Studio
    
    Example: A member might be "John Doe", "Lead Programmer", working at "CD Projekt Red"
    """
    
    _name = 'game.member'  # Database table: game_member
    _columns = {
        'name': fields.char(
            'Tên nhân viên',
            size=25,
            required=True
        ),
        # Employee's full name
        # Example: 'Adam Badowski', 'Naoki Yoshida', 'Neil Druckmann'
        
        'role': fields.char(
            'Chức vụ',
            size=25
        ),
        # Job title/position at the studio
        # Example: 'Lead Game Designer', 'Senior Programmer', 'Art Director'
        # Note: Optional field - can be null if role is not specified
        
        # ===== PARENT RELATIONSHIP (many2one) =====
        # many2one creates a child-to-parent relationship:
        # - A Member belongs to ONE Studio
        # - Many Members can belong to the same Studio
        # - Stores the studio_id as a foreign key in game_member table
        # - In XML: displayed as a dropdown selector in the form
        
        'studio_id': fields.many2one(
            'game.studio',     # Target model (the parent model)
            'Nhà phát triển'   # Field label (Vietnamese: "Development Studio")
        ),
        # Points to the studio where this member works
        # The studio also has a reverse one2many link (members field)
        # to show all its members
    }


class Genre(osv.Model):
    """
    GENRE MODEL - Manages game genre categories
    
    Represents a game genre/category that can be assigned to games.
    This is a reference table for genre definitions.
    
    Note: Currently, the Game model uses a selection field for genre instead of
    linking to this model. Consider refactoring Game.genre to use many2one or
    many2many relationship to this model for better flexibility.
    
    Example: 'Action', 'RPG', 'Strategy', 'Puzzle'
    """
    
    _name = 'game.genre'  # Database table: game_genre
    _columns = {
        'name': fields.char(
            'Tên thể loại',
            size=25,
            required=True
        ),
        # Genre name
        # Example: 'Action-Adventure', 'Tactical RPG', 'Roguelike'
    }


class Platform(osv.Model):
    """
    PLATFORM MODEL - Manages gaming platforms/systems
    
    Represents a gaming platform/system where games can be played.
    Games link to platforms via many2many relationship.
    
    Relationships:
    - Implicit many2many: Connected to Game via game_platform_rel junction table
    
    Example: 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch', 'PC'
    """
    
    _name = 'game.platform'  # Database table: game_platform
    _columns = {
        'name': fields.char(
            'Tên máy tính',
            size=25,
            required=True
        ),
        # Platform/system name
        # Example: 'Windows PC', 'PlayStation 5', 'Nintendo Switch', 'Steam Deck'
    }


class Series(osv.Model):
    """
    SERIES MODEL - Manages game series/franchises
    
    Represents a game series/franchise that can contain multiple game titles.
    One series can have many games (one2many relationship with Game model).
    
    Relationships:
    - one2many: Implicit relationship with Game (games have series_id pointing here)
    
    Example: 'The Witcher' series contains The Witcher 1, 2, 3, 4 (future)
    """
    
    _name = 'game.series'  # Database table: game_series
    _columns = {
        'name': fields.char(
            'Tên series',
            size=25,
            required=True
        ),
        # Series/franchise name
        # Example: 'The Witcher', 'Final Fantasy', 'Elder Scrolls'
        
        'description': fields.text('Mô tả'),
        # Detailed description of the series/franchise
        # Example: "A fantasy action RPG series set in the Northern Kingdoms..."
    }
