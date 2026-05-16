# OpenERP v7 Game Management Module - Developer Knowledge Base

A comprehensive technical reference for developing and maintaining the Game Management module using OpenERP v7's legacy ORM patterns and XML view architecture.

---

## 1. Legacy ORM Syntax (osv.osv) - The Foundation

### What is OSV (Object Services)?

**OSV** is OpenERP v7's object-relational mapping (ORM) layer. It maps Python classes to database tables automatically. Unlike modern Odoo (v12+) which uses Python class inheritance, v7 uses a dictionary-based `_columns` pattern.

### Core Pattern: _name and _columns

Every model requires two essential attributes:

```python
from openerp.osv import fields, osv

class Game(osv.Model):
    """Represents a video game title in the database"""
    
    _name = 'game.game'  # Database table: game_game (underscores become table names)
    _columns = {
        # All fields defined here
    }
```

**What happens behind the scenes:**
- `_name = 'game.game'` → Creates/maps to database table `game_game`
- The module name (`game`) becomes the schema prefix
- OpenERP automatically creates primary key (`id`) and timestamps (`create_date`, `write_date`)
- Each field in `_columns` becomes a database column

### Game Model Example:

```python
class Game(osv.Model):
    _name = 'game.game'
    _columns = {
        'name': fields.char('Tên game', size=25, required=True, translate=True),
        'price': fields.float('Giá'),
        'status': fields.selection([
            ('released', 'Đã phát hành'),
            ('upcoming', 'Sắp phát hành'),
        ], 'Trạng thái', required=True),
    }
```

**Data Flow:**
1. User creates a game "The Witcher 3" in the UI
2. OpenERP ORM calls the model's `create()` method (inherited)
3. Data is validated against field definitions
4. SQL INSERT is generated: `INSERT INTO game_game (name, price, status) VALUES (...)`
5. The new record's `id` is returned

---

## 2. Relational Fields - Connecting Models

OpenERP's power comes from its relational field types. They automatically manage foreign keys and cross-model queries.

### 2.1 many2one: Parent-Child Relationship (One Belongs To One)

**Concept:** A Game **belongs to** ONE Publisher. A Publisher can have MANY Games.

```python
class Game(osv.Model):
    _name = 'game.game'
    _columns = {
        'name': fields.char('Tên game', size=25, required=True),
        
        # Many2One: This game has ONE publisher
        'publisher_id': fields.many2one(
            'game.publisher',  # Target model
            'Nhà phát hành'    # Field label (Vietnamese: "Publisher")
        ),
    }

class Publisher(osv.Model):
    _name = 'game.publisher'
    _columns = {
        'name': fields.char('Tên nhà phát hành', size=25, required=True),
        # Note: Publisher does NOT define an explicit reverse field
        # But you can still query "all games by this publisher" using ORM methods
    }
```

**Database Impact:**
- `game_game` table gets a new column: `publisher_id` (foreign key)
- When you create a game, you select a publisher from a dropdown
- When you delete a publisher, OpenERP handles cascade behavior

**Real-world Example:**
```
Game: "Baldur's Gate 3"  ─┐
Game: "Dark Suns"        ─┼─→ Publisher: "Larian Studios"
Game: "Divinity OS"      ─┘
```

**Practical Code (Form View):**
```xml
<field name="publisher_id" string="Nhà phát hành:"/>
<!-- Renders as a dropdown selector showing all game.publisher records -->
```

### 2.2 one2many: Parent-Children Relationship (Reverse of many2one)

**Concept:** A Studio **has MANY** Members. Each Member belongs to ONE Studio.

```python
class Studio(osv.Model):
    _name = 'game.studio'
    _columns = {
        'name': fields.char('Tên nhà phát triển', size=25, required=True),
        
        # One2Many: This studio has MANY members
        'members': fields.one2many(
            'game.member',     # Target model (the child model)
            'studio_id',       # Foreign key column in game_member pointing to this studio
            'Nhân viên'        # Field label (Vietnamese: "Employees")
        ),
    }

class Member(osv.Model):
    _name = 'game.member'
    _columns = {
        'name': fields.char('Tên nhân viên', size=25, required=True),
        'role': fields.char('Chức vụ', size=25),
        
        # This is the "other side" of the one2many relationship
        'studio_id': fields.many2one(
            'game.studio',
            'Nhà phát triển'
        ),
    }
```

**Key Understanding:**
- **one2many is a VIRTUAL field** – it doesn't store data in the Studio table
- It queries the Member table: `SELECT * FROM game_member WHERE studio_id = <this_studio_id>`
- The actual foreign key is in the Member table (`studio_id`)
- **Relationship is defined backward:** `one2many` points to the foreign key column in the child model

**Real-world Example:**
```
Studio: "FromSoftware" has members:
  ├─ Member: "Hidetaka Miyazaki" (Director)
  ├─ Member: "Yui Tanimura" (Producer)
  └─ Member: "Tsukasa Takenaka" (Art Director)
```

**Practical Code (Form View with Embedded Tree):**
```xml
<notebook>
    <page string="Nhân viên">
        <!-- Embedded tree allows viewing/editing members without leaving the studio form -->
        <field name="members">
            <tree string="Danh sách nhân viên" editable="bottom">
                <field name="name"/>
                <field name="role"/>
            </tree>
        </field>
    </page>
</notebook>
```

Users can:
- Add new members directly in this embedded tree
- Edit member details inline
- Delete members without opening a separate form

### 2.3 many2many: Peer-to-Peer Relationship (M:N)

**Concept:** A Game is available on MANY Platforms. A Platform hosts MANY Games.

```python
class Game(osv.Model):
    _name = 'game.game'
    _columns = {
        'name': fields.char('Tên game', size=25, required=True),
        
        # Many2Many: This game is on MANY platforms
        'platforms': fields.many2many(
            'game.platform',           # Target model
            'game_platform_rel',       # Junction table name (OpenERP creates it)
            'game_id',                 # Column in junction pointing to games
            'platform_id',             # Column in junction pointing to platforms
            'Máy tính'                 # Field label (Vietnamese: "Platforms")
        ),
    }

class Platform(osv.Model):
    _name = 'game.platform'
    _columns = {
        'name': fields.char('Tên máy tính', size=25, required=True),
        # Note: No explicit reverse many2many field needed
        # You can still query "all games on this platform" using ORM methods
    }
```

**Database Impact:**
- Creates a junction table: `game_platform_rel`
- Columns: `game_id`, `platform_id`, `id`
- Example data:
  ```
  game_platform_rel:
  ┌─────────┬─────────────┐
  │ game_id │ platform_id │
  ├─────────┼─────────────┤
  │ 1       │ 1           │  // "Elden Ring" on "PC"
  │ 1       │ 3           │  // "Elden Ring" on "PlayStation 5"
  │ 2       │ 1           │  // "Baldur's Gate 3" on "PC"
  └─────────┴─────────────┘
  ```

**Real-world Example:**
```
Game: "The Witcher 3" is on:
  ├─ Platform: "PC (Windows)"
  ├─ Platform: "PlayStation 4"
  ├─ Platform: "Xbox One"
  ├─ Platform: "Nintendo Switch"
  └─ Platform: "PlayStation 5"
```

**Practical Code (Form View with Many2Many Tags Widget):**
```xml
<field name="platforms" 
       widget="many2many_tags"
       string="Nền tảng chơi:"
       colspan="4"/>
```

The `widget="many2many_tags"` attribute creates a modern tag-based UI where:
- Users see selected platforms as colored tags
- They can click an "x" to remove a platform
- They can type to search and add new platforms
- Modern, clean interface compared to dropdown menus

---

## 3. Field Types Reference (Game Module Context)

### Character Fields (Text)

```python
'name': fields.char('Tên game', size=25, required=True, translate=True)
```
- **size=25**: Max 25 characters (database VARCHAR(25))
- **required=True**: Cannot be empty (enforced at ORM level)
- **translate=True**: Values stored in translations table for multi-language support

**Used in Game Module:**
- `game.game.name` – Game title
- `game.publisher.name` – Publisher name
- `game.studio.name` – Studio name

### Text Fields (Large Text)

```python
'description': fields.text('Mô tả')
'notes': fields.text('Chi tiết')
```
- **No size limit** – Can store thousands of characters
- Renders as `<textarea>` in UI
- Ideal for descriptions, notes, long content

**Used in Game Module:**
- `game.game.description` – Full game synopsis
- `game.game.notes` – Technical details, system requirements
- `game.series.description` – Series history and lore

### Selection Fields (Dropdown)

```python
'genre': fields.selection([
    ('action', 'Hành động'),
    ('rpg', 'Nhập vai'),
    ('fps', 'Bắn súng'),
], 'Thể loại', required=True)

'status': fields.selection([
    ('released', 'Đã phát hành'),
    ('upcoming', 'Sắp phát hành'),
    ('cancelled', 'Đã hủy')
], 'Trạng thái', required=True)
```
- **Format:** `('database_value', 'Display Label')`
- Returns the database value (e.g., 'action', 'released')
- Limited to predefined choices

**Important Note:** The Game model uses a selection field for genre. For better flexibility (allowing multiple genres per game), consider refactoring to `many2many('game.genre')`.

### Numeric Fields

```python
'price': fields.float('Giá')      # Decimal numbers (59.99, 29.99)
'rating': fields.integer('Đánh giá')  # Whole numbers
```

**Used in Game Module:**
- `game.game.price` – Game retail price

### DateTime Fields

```python
'release_date': fields.datetime('Ngày phát hành')
```
- Stores date and time: `YYYY-MM-DD HH:MM:SS`
- UI renders as a date picker with time selector
- Useful for game release dates, schedule tracking

---

## 4. XML Layouts - Creating User-Friendly Forms

### 4.1 Sheet Wrapper (Paper UI)

The `<sheet>` tag is **mandatory** for OpenERP v7 form design. It creates the characteristic paper-like container.

```xml
<form string="Nhà phát triển">
    <sheet>
        <!-- All form content goes inside <sheet> -->
        <group col="2">
            <field name="name"/>
        </group>
    </sheet>
</form>
```

**Without `<sheet>`:** Form looks plain and unstyled
**With `<sheet>`:** Clean, professional paper-like appearance with shadows and spacing

### 4.2 Group Layout (Field Organization)

Groups organize fields into logical columns.

```xml
<sheet>
    <!-- col="2" creates 2 columns -->
    <group col="2" string="Thông tin cơ bản">
        <field name="name"/>
        <field name="price"/>
        <!-- These two fields appear side-by-side in 2 columns -->
    </group>

    <!-- col="4" creates 4 columns (wider layout) -->
    <group col="4" string="Chi tiết phát hành">
        <field name="release_date"/>
        <field name="status"/>
        <field name="publisher_id"/>
        <field name="studio_id"/>
    </group>
</sheet>
```

**Real Layout Example (Game Form):**
```
┌─────────────────────────────────────┐
│  Tên game                             │
├─────────────────────────────────────┤
│  Thể loại    │    Trạng thái         │
│  Ngày phát   │    Giá                │
├─────────────────────────────────────┤
│  Nhà phát hành:                       │
│  Nhà phát triển:                      │
└─────────────────────────────────────┘
```

### 4.3 Colspan (Spanning Multiple Columns)

```xml
<group col="2">
    <field name="name" colspan="2"/>  <!-- Takes full width (2 columns) -->
    <field name="price"/>             <!-- Takes 1 column (left) -->
    <field name="status"/>            <!-- Takes 1 column (right) -->
</group>
```

---

## 5. Notebooks & Inline Tree Editing

### 5.1 Notebooks (Tabbed Interface)

Notebooks organize complex forms into tabs for better UX.

```xml
<form string="Game Information">
    <sheet>
        <!-- Main fields -->
        <group col="2">
            <field name="name"/>
            <field name="price"/>
        </group>

        <!-- Tabbed interface for additional info -->
        <notebook>
            <!-- Tab 1: Description -->
            <page string="Mô tả">
                <field name="description" nolabel="1"/>
            </page>

            <!-- Tab 2: Details -->
            <page string="Chi tiết">
                <field name="notes" nolabel="1"/>
            </page>
        </notebook>
    </sheet>
</form>
```

**User Experience:**
- Users see tabs at the top: "Mô tả", "Chi tiết"
- Clicking a tab switches content without leaving the form
- Main fields always visible, secondary info in tabs

### 5.2 Inline Tree Editing (one2many with editable="bottom")

Embed a child list directly in a parent form with inline editing.

```xml
<form string="Nhà phát triển">
    <sheet>
        <group col="2">
            <field name="name"/>
            <field name="headquarter"/>
        </group>

        <notebook>
            <page string="Nhân viên">
                <!-- Embed the one2many relationship as an editable tree -->
                <field name="members">
                    <tree string="Danh sách nhân viên" editable="bottom">
                        <field name="name"/>
                        <field name="role"/>
                        <!-- Note: studio_id is implicit, not shown -->
                    </tree>
                </field>
            </page>
        </notebook>
    </sheet>
</form>
```

**What `editable="bottom"` does:**
- Users can add new members by clicking the last empty row
- Users can edit member fields directly in the tree (no separate form)
- Users can delete rows with a right-click context menu
- Changes are saved when you save the parent studio record

**Real Studio Form Workflow:**
1. Open "FromSoftware" studio record
2. Go to "Nhân viên" tab
3. See embedded tree with existing members
4. Click last empty row to add new member
5. Type name and role inline
6. Save the studio – member is saved with `studio_id` automatically set

---

## 6. UI Widgets - Enhanced Field Rendering

### 6.1 Many2Many Rendering

**OpenERP v7 Standard:**

```xml
<field name="platforms" 
       string="Nền tảng chơi:"
       colspan="4"/>
```

OpenERP v7 renders many2many fields as a standard selection interface (checkboxes or list view).

**Important:** The `widget="many2many_tags"` attribute is **NOT supported in OpenERP v7**. It was introduced in Odoo v9+. Using it will cause:
```
AttributeError: 'NoneType' object has no attribute '_name_search'
```

**User Experience in v7:**
- Many2many fields display as checkboxes in form views
- Users can multi-select available platforms
- Changes are saved to the junction table automatically
- No tag-based UI, but fully functional

**Real-world Example:**
```
Platforms: 
  ☑ PC (Windows)
  ☑ PlayStation 5
  ☐ Xbox Series X
  ☑ Nintendo Switch
  ☐ Steam Deck
```

### 6.2 Selection Widget (Explicit)

```xml
<field name="status" string="Trạng thái:"/>
<!-- Renders as dropdown with predefined choices -->
```

---

## 7. Search Views - Filtering and Searching

Search views allow users to find and filter records.

```xml
<record model="ir.ui.view" id="view_game_search">
    <field name="name">game.search</field>
    <field name="model">game.game</field>
    <field name="type">search</field>
    <field name="arch" type="xml">
        <search string="Tìm kiếm game">
            <!-- Searchable fields -->
            <field name="name" string="Tên game"/>
            <field name="genre" string="Thể loại"/>
            <field name="publisher_id" string="Nhà phát hành"/>
            
            <!-- Separator for logical grouping -->
            <separator/>
            
            <!-- Quick filters (predefined domain queries) -->
            <filter name="released" string="Đã phát hành" 
                    domain="[('status','=','released')]"/>
            <filter name="upcoming" string="Sắp phát hành" 
                    domain="[('status','=','upcoming')]"/>
        </search>
    </field>
</record>
```

**User Can:**
- Type in the search box to filter by name
- Click "Thể loại" to filter by genre
- Click "Nhà phát hành" to filter by publisher
- Click "Đã phát hành" button for quick filter

---

## 8. Tree Views (List Views)

Tree views display records in a table format.

```xml
<record model="ir.ui.view" id="view_game_tree">
    <field name="name">game.tree</field>
    <field name="model">game.game</field>
    <field name="type">tree</field>
    <field name="arch" type="xml">
        <tree string="Danh sách các tựa game">
            <field name="name"/>
            <field name="studio_id"/>
            <field name="publisher_id"/>
            <field name="genre"/>
            <field name="release_date"/>
            <field name="status"/>
            <field name="price"/>
        </tree>
    </field>
</record>
```

**With Inline Editing:**
```xml
<tree string="Danh sách nhân viên" editable="bottom">
    <field name="name"/>
    <field name="role"/>
</tree>
```

Users can edit fields directly without opening forms.

---

## 9. Window Actions - Linking Views to the Menu

Window Actions connect views to the menu system and define default behaviors.

```xml
<!-- CRITICAL: Window Actions must be defined BEFORE menuitem tags reference them -->
<!-- Otherwise: ValueError: External ID not found -->

<record model="ir.actions.act_window" id="action_game">
    <field name="name">Thông tin Game</field>
    <field name="res_model">game.game</field>
    <field name="view_type">form</field>
    <field name="view_mode">tree,form</field>
    <!-- view_mode order: tree (list) appears first, form (detail) second -->
</record>

<record model="ir.actions.act_window" id="action_studio">
    <field name="name">Nhà phát triển</field>
    <field name="res_model">game.studio</field>
    <field name="view_type">form</field>
    <field name="view_mode">tree,form</field>
</record>
```

**Later, in game_menu.xml:**
```xml
<menuitem id="menu_game_root" name="Game Management"/>
<menuitem id="menu_game" name="Games" 
          parent="menu_game_root"
          action="action_game"/>
```

---

## 10. Complete Example: Game Form Walkthrough

Here's a complete, production-ready form structure:

```xml
<record model="ir.ui.view" id="view_game_form">
    <field name="name">game.form</field>
    <field name="model">game.game</field>
    <field name="type">form</field>
    <field name="arch" type="xml">
        <form string="Thông tin Game">
            <!-- Sheet: Mandatory container -->
            <sheet>
                <!-- Header: Game Title -->
                <group col="4">
                    <field name="name" colspan="4" string="Tên game:"/>
                </group>

                <!-- Group 1: Core Information (2 columns) -->
                <group col="2" string="Thông tin cơ bản">
                    <field name="genre" string="Thể loại:"/>
                    <field name="status" string="Trạng thái:"/>
                    <field name="release_date" string="Ngày phát hành:"/>
                    <field name="price" string="Giá:"/>
                </group>

                <!-- Group 2: Organization Links (2 columns) -->
                <group col="2" string="Thông tin phát hành">
                    <field name="publisher_id" string="Nhà phát hành:"/>
                    <field name="studio_id" string="Nhà phát triển:"/>
                    <field name="series_id" string="Series:"/>
                </group>

                <!-- Many2Many Tags: Platforms -->
                <group col="4">
                    <field name="platforms" 
                           widget="many2many_tags"
                           string="Nền tảng chơi:"
                           colspan="4"/>
                </group>

                <!-- Notebooks: Detailed Information -->
                <notebook>
                    <!-- Tab 1: Full Description -->
                    <page string="Mô tả">
                        <field name="description" nolabel="1"/>
                    </page>

                    <!-- Tab 2: Technical Details -->
                    <page string="Chi tiết">
                        <field name="notes" nolabel="1" 
                               placeholder="Thêm các chi tiết bổ sung..."/>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

---

## 11. Common Patterns & Best Practices

### Pattern 1: Embedded Child Management

Instead of switching to a different view, manage related records inline:

```xml
<form string="Studio">
    <sheet>
        <group col="2">
            <field name="name"/>
            <field name="headquarter"/>
        </group>
        <notebook>
            <page string="Members">
                <field name="members">
                    <tree editable="bottom">
                        <field name="name"/>
                        <field name="role"/>
                    </tree>
                </field>
            </page>
        </notebook>
    </sheet>
</form>
```

**Benefit:** Users manage members without leaving the studio form.

### Pattern 2: Deduplicating Choice Lists

Remove duplicates from selection fields:

```python
'genre': fields.selection([
    ('action', 'Hành động'),
    ('rpg', 'Nhập vai'),
    ('fps', 'Bắn súng'),
    # Remove: ('rpg', 'Nhập vai'),  # Duplicate!
    # Instead: refactor to many2many('game.genre')
], 'Thể loại', required=True)
```

**Better Solution:** Use many2many for flexible genre assignment.

### Pattern 3: Placeholder Text for Guidance

Help users fill fields correctly:

```xml
<field name="notes" 
       placeholder="Thêm các chi tiết bổ sung về tựa game..."/>
<!-- Lighter text shown when field is empty -->
```

---

## 12. Critical Execution Order Rules

**Rule #1: Window Actions Before Menu Items**

```xml
<!-- ✓ CORRECT: Define action first -->
<record model="ir.actions.act_window" id="action_game">
    ...
</record>

<!-- Then reference it in menu -->
<menuitem action="action_game" .../>

<!-- ✗ WRONG: Reference before defining -->
<menuitem action="action_game" .../>  <!-- ERROR: External ID not found -->
<record model="ir.actions.act_window" id="action_game">
    ...
</record>
```

**Rule #2: View IDs in Actions**

When referring to specific views:

```xml
<record model="ir.actions.act_window" id="action_game">
    <field name="view_ids" eval="[(6, 0, [ref('view_game_tree'), ref('view_game_form')])]"/>
</record>
```

**Rule #3: Module Dependencies**

Ensure dependent modules are listed in `__openerp__.py`:

```python
{
    'depends': ['base'],  # Always include base
}
```

---

## 13. Game Module Data Flow Example

### Scenario: Creating a Game Record

1. **User navigates to Games menu** → Loads `action_game`
2. **Tree view appears** → Queries `game.game` model
3. **User clicks "Create"** → Form view opens (empty record)
4. **User enters game name** → "The Witcher 3"
5. **User selects publisher** → Dropdown queries `game.publisher`
6. **User selects studio** → Dropdown queries `game.studio`
7. **User selects platforms** → Many2Many tag selector queries `game.platform`
8. **User enters description/notes** → In notebook tabs
9. **User clicks "Save"** → ORM validates all required fields
10. **Database INSERT executed**:
    ```sql
    INSERT INTO game_game 
    (name, description, genre, release_date, status, notes, price, 
     publisher_id, studio_id, series_id)
    VALUES (...)
    ```
11. **Junction records created** for platforms:
    ```sql
    INSERT INTO game_platform_rel (game_id, platform_id) VALUES (...)
    ```
12. **Record ID returned** → Record opens in form view
13. **Junction table queried** → Platforms displayed as tags

---

## 14. Quick Reference: Game Module Models

| Model | Table | Purpose | Key Relationships |
|-------|-------|---------|-------------------|
| `game.game` | `game_game` | Video game title | many2one(Publisher, Studio, Series), many2many(Platform) |
| `game.publisher` | `game_publisher` | Game distributor | Implicit one2many with Game |
| `game.studio` | `game_studio` | Development company | one2many(Member) |
| `game.member` | `game_member` | Employee at studio | many2one(Studio) |
| `game.genre` | `game_genre` | Game category | Reference table (not linked) |
| `game.platform` | `game_platform` | Gaming system | Implicit many2many with Game |
| `game.series` | `game_series` | Game franchise | Implicit one2many with Game |

---

## 15. Debugging Tips

### View Not Appearing

```xml
<!-- Problem: View not showing in dropdown -->
<!-- Solution: Check view_mode order in action -->
<field name="view_mode">tree,form</field>  <!-- ✓ Tree first, then form -->
<field name="view_mode">form,tree</field>  <!-- ✓ Also valid -->
```

### Field Not Showing

```xml
<!-- Problem: Field defined in model but missing in form -->
<!-- Solution: Add explicit <field> tag -->
<form>
    <sheet>
        <field name="name"/>  <!-- ✓ Now visible -->
    </sheet>
</form>
```

### Many2One Dropdown Empty

```python
# Problem: Dropdown shows no options
# Solution: Check target model has records or required=False

'publisher_id': fields.many2one('game.publisher', 'Nhà phát hành')
# ✓ Works when game.publisher has records
# ✓ Dropdown is empty if no publishers exist
```

---

## Conclusion

The Game Management module demonstrates OpenERP v7's complete development stack:
- **Python ORM:** Model definitions with fields and relationships
- **XML UI:** Forms, trees, searches with clean, organized layouts
- **Database:** Automatic table/column creation with relational integrity
- **User Experience:** Intuitive interfaces with tabs, inline editing, and tag selectors

Master these patterns and you can build any business application in OpenERP v7.