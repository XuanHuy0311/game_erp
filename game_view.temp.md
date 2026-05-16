<?xml version="1.0" encoding="utf-8"?>
<openerp>
    <data>
        <!-- ====================================================================
             GAME MANAGEMENT - SEARCH VIEWS, TREE VIEWS, FORM VIEWS, AND ACTIONS
             ==================================================================== -->

        <!-- ============================================================================
             GAME MODEL VIEWS
             ============================================================================ -->

        <!-- GAME Search View -->
        <record model="ir.ui.view" id="view_game_search">
            <field name="name">game.search</field>
            <field name="model">game.game</field>
            <field name="type">search</field>
            <field name="arch" type="xml">
                <search string="Tìm kiếm game">
                    <!-- Primary search field for game title -->
                    <field name="name" string="Tên game"/>
                    
                    <!-- Genre filter - allows filtering by game category -->
                    <field name="genre" string="Thể loại"/>
                    
                    <!-- Publisher filter - narrow down by publishing company -->
                    <field name="publisher_id" string="Nhà phát hành"/>
                    
                    <!-- Status filter - released, upcoming, or cancelled -->
                    <field name="status" string="Trạng thái"/>
                    
                    <!-- Studio filter - find games by development team -->
                    <field name="studio_id" string="Nhà phát triển"/>
                    
                    <!-- Separators for logical grouping in the filter dropdown -->
                    <separator/>
                    <filter name="released_games" string="Đã phát hành" domain="[('status','=','released')]"/>
                    <filter name="upcoming_games" string="Sắp phát hành" domain="[('status','=','upcoming')]"/>
                </search>
            </field>
        </record>

        <!-- GAME Tree View (List View) -->
        <record model="ir.ui.view" id="view_game_tree">
            <field name="name">game.tree</field>
            <field name="model">game.game</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree string="Danh sách các tựa game">
                    <field name="name"/>              <!-- Game title -->
                    <field name="studio_id"/>         <!-- Developer -->
                    <field name="publisher_id"/>      <!-- Publisher -->
                    <field name="genre"/>             <!-- Genre/category -->
                    <field name="release_date"/>      <!-- Release date -->
                    <field name="status"/>            <!-- Current status -->
                    <field name="price"/>             <!-- Game price -->
                </tree>
            </field>
        </record>

        <!-- GAME Form View (Main Detail Form with Sheet and Notebook) -->
        <record model="ir.ui.view" id="view_game_form">
            <field name="name">game.form</field>
            <field name="model">game.game</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="Thông tin Game">
                    <!-- <sheet> wrapper creates the paper-like UI container in OpenERP v7
                         All form content must be wrapped inside <sheet> for proper styling -->
                    <sheet>
                        <!-- ===== HEADER ROW: Game Title ===== -->
                        <group col="4">
                            <field name="name" colspan="4" string="Tên game:"/>
                        </group>

                        <!-- ===== FIRST GROUP: Basic Game Information ===== -->
                        <group col="2" string="Thông tin cơ bản">
                            <!-- Left column: Genre and Status -->
                            <field name="genre" 
                                   widget="selection" 
                                   string="Thể loại:"/>
                            <field name="status" string="Trạng thái:"/>
                            
                            <!-- Right column: Release Date and Price -->
                            <field name="release_date" string="Ngày phát hành:"/>
                            <field name="price" string="Giá:"/>
                        </group>

                        <!-- ===== SECOND GROUP: Organization/Production Links ===== -->
                        <group col="2" string="Thông tin phát hành">
                            <!-- Many2One relationships to publisher and studio -->
                            <field name="publisher_id" string="Nhà phát hành:"/>
                            <field name="studio_id" string="Nhà phát triển:"/>
                            <field name="series_id" string="Series:"/>
                        </group>

                        <!-- ===== PLATFORMS: Many2Many with Tags Widget ===== -->
                        <group col="4">
                            <field name="platforms" 
                                   widget="many2many_tags"
                                   string="Nền tảng chơi:"
                                   colspan="4"/>
                            <!-- widget="many2many_tags" provides a modern tag-based UI for selecting
                                 multiple platforms (PC, PS5, Xbox, etc.) instead of a dropdown -->
                        </group>

                        <!-- ===== NOTEBOOK: Tabbed interface for detailed information ===== -->
                        <notebook>
                            <!-- TAB 1: Description -->
                            <page string="Mô tả">
                                <field name="description" nolabel="1"/>
                                <!-- Large text field for full game description/synopsis -->
                            </page>

                            <!-- TAB 2: Additional Details/Notes -->
                            <page string="Chi tiết">
                                <field name="notes" nolabel="1" placeholder="Thêm các chi tiết bổ sung về tựa game..."/>
                                <!-- Placeholder provides user guidance when the field is empty -->
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- GAME Action Window (links the view to menu system) -->
        <record model="ir.actions.act_window" id="action_game">
            <field name="name">Thông tin Game</field>
            <field name="res_model">game.game</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <!-- view_mode order: tree (list) first, then form (detail) -->
        </record>

        <!-- ============================================================================
             PUBLISHER MODEL VIEWS
             ============================================================================ -->

        <!-- PUBLISHER Search View -->
        <record model="ir.ui.view" id="view_publisher_search">
            <field name="name">publisher.search</field>
            <field name="model">game.publisher</field>
            <field name="type">search</field>
            <field name="arch" type="xml">
                <search string="Tìm kiếm Nhà phát hành">
                    <field name="name" string="Tên"/>
                    <field name="country" string="Quốc gia"/>
                </search>
            </field>
        </record>

        <!-- PUBLISHER Tree View (List - Editable Bottom) -->
        <record model="ir.ui.view" id="view_publisher_tree">
            <field name="name">publisher.tree</field>
            <field name="model">game.publisher</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <!-- editable="bottom" allows inline editing without opening the form
                     Users can create new records and edit existing ones directly in the list -->
                <tree string="Danh sách Nhà phát hành" editable="bottom">
                    <field name="name"/>        <!-- Publisher name -->
                    <field name="country"/>    <!-- Country of origin -->
                </tree>
            </field>
        </record>

        <!-- PUBLISHER Form View -->
        <record model="ir.ui.view" id="view_publisher_form">
            <field name="name">publisher.form</field>
            <field name="model">game.publisher</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="Nhà phát hành">
                    <sheet>
                        <!-- <group> layout: col="2" creates a 2-column layout
                             Fields align vertically in columns for better visual organization -->
                        <group col="2" string="Thông tin nhà phát hành">
                            <field name="name" string="Tên:"/>
                            <field name="country" string="Quốc gia:"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- PUBLISHER Action Window -->
        <record model="ir.actions.act_window" id="action_publisher">
            <field name="name">Nhà phát hành</field>
            <field name="res_model">game.publisher</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

        <!-- ============================================================================
             STUDIO MODEL VIEWS (with embedded Member tree view)
             ============================================================================ -->

        <!-- STUDIO Search View -->
        <record model="ir.ui.view" id="view_studio_search">
            <field name="name">studio.search</field>
            <field name="model">game.studio</field>
            <field name="type">search</field>
            <field name="arch" type="xml">
                <search string="Tìm kiếm Nhà phát triển">
                    <field name="name" string="Tên"/>
                    <field name="headquarter" string="Trụ sở chính"/>
                </search>
            </field>
        </record>

        <!-- STUDIO Tree View -->
        <record model="ir.ui.view" id="view_studio_tree">
            <field name="name">studio.tree</field>
            <field name="model">game.studio</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree string="Danh sách Nhà phát triển">
                    <field name="name"/>           <!-- Studio name -->
                    <field name="headquarter"/>   <!-- Headquarters location -->
                </tree>
            </field>
        </record>

        <!-- STUDIO Form View (with one2many Members embedded in Notebook) -->
        <record model="ir.ui.view" id="view_studio_form">
            <field name="name">studio.form</field>
            <field name="model">game.studio</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="Nhà phát triển">
                    <sheet>
                        <!-- Basic studio information -->
                        <group col="2" string="Thông tin chung">
                            <field name="name" string="Tên:"/>
                            <field name="headquarter" string="Trụ sở chính:"/>
                        </group>

                        <!-- ===== NOTEBOOK for Members (one2many relationship) ===== -->
                        <notebook>
                            <!-- TAB: List of employees working at this studio
                                 The 'members' field is a one2many relationship that shows all
                                 game.member records where studio_id matches this studio -->
                            <page string="Nhân viên">
                                <!-- Embedded tree view with editable="bottom" for inline member creation/editing -->
                                <field name="members">
                                    <tree string="Danh sách nhân viên" editable="bottom">
                                        <field name="name" string="Tên"/>
                                        <field name="role" string="Chức vụ"/>
                                        <!-- studio_id is not shown because it's implicit (already this studio) -->
                                    </tree>
                                </field>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- STUDIO Action Window -->
        <record model="ir.actions.act_window" id="action_studio">
            <field name="name">Nhà phát triển</field>
            <field name="res_model">game.studio</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

        <!-- ============================================================================
             MEMBER MODEL VIEWS
             ============================================================================ -->

        <!-- MEMBER Search View -->
        <record model="ir.ui.view" id="view_member_search">
            <field name="name">member.search</field>
            <field name="model">game.member</field>
            <field name="type">search</field>
            <field name="arch" type="xml">
                <search string="Tìm kiếm Nhân viên">
                    <field name="name" string="Tên"/>
                    <field name="role" string="Chức vụ"/>
                    <field name="studio_id" string="Nhà phát triển"/>
                </search>
            </field>
        </record>

        <!-- MEMBER Tree View -->
        <record model="ir.ui.view" id="view_member_tree">
            <field name="name">member.tree</field>
            <field name="model">game.member</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree string="Danh sách nhân viên">
                    <field name="name"/>            <!-- Member name -->
                    <field name="role"/>            <!-- Job title -->
                    <field name="studio_id"/>       <!-- Associated studio -->
                </tree>
            </field>
        </record>

        <!-- MEMBER Form View -->
        <record model="ir.ui.view" id="view_member_form">
            <field name="name">member.form</field>
            <field name="model">game.member</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="Nhân viên">
                    <sheet>
                        <group col="2" string="Thông tin nhân viên">
                            <field name="name" string="Tên:"/>
                            <field name="role" string="Chức vụ:"/>
                            <field name="studio_id" string="Nhà phát triển:"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- MEMBER Action Window -->
        <record model="ir.actions.act_window" id="action_member">
            <field name="name">Nhân viên</field>
            <field name="res_model">game.member</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

        <!-- ============================================================================
             GENRE MODEL VIEWS
             ============================================================================ -->

        <!-- GENRE Search View -->
        <record model="ir.ui.view" id="view_genre_search">
            <field name="name">genre.search</field>
            <field name="model">game.genre</field>
            <field name="type">search</field>
            <field name="arch" type="xml">
                <search string="Tìm kiếm Thể loại">
                    <field name="name" string="Tên thể loại"/>
                </search>
            </field>
        </record>

        <!-- GENRE Tree View (Editable for quick inline management) -->
        <record model="ir.ui.view" id="view_genre_tree">
            <field name="name">genre.tree</field>
            <field name="model">game.genre</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <!-- editable="bottom": Users can add and edit genres directly in the list view -->
                <tree string="Danh sách thể loại" editable="bottom">
                    <field name="name" string="Tên thể loại"/>
                </tree>
            </field>
        </record>

        <!-- GENRE Form View -->
        <record model="ir.ui.view" id="view_genre_form">
            <field name="name">genre.form</field>
            <field name="model">game.genre</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="Thể loại Game">
                    <sheet>
                        <group col="2">
                            <field name="name" string="Tên thể loại:"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- GENRE Action Window -->
        <record model="ir.actions.act_window" id="action_genre">
            <field name="name">Thể loại</field>
            <field name="res_model">game.genre</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

        <!-- ============================================================================
             PLATFORM MODEL VIEWS
             ============================================================================ -->

        <!-- PLATFORM Search View -->
        <record model="ir.ui.view" id="view_platform_search">
            <field name="name">platform.search</field>
            <field name="model">game.platform</field>
            <field name="type">search</field>
            <field name="arch" type="xml">
                <search string="Tìm kiếm Nền tảng">
                    <field name="name" string="Tên nền tảng"/>
                </search>
            </field>
        </record>

        <!-- PLATFORM Tree View (Editable for quick inline management) -->
        <record model="ir.ui.view" id="view_platform_tree">
            <field name="name">platform.tree</field>
            <field name="model">game.platform</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <!-- editable="bottom": Users can add and edit platforms directly in the list view -->
                <tree string="Danh sách nền tảng" editable="bottom">
                    <field name="name" string="Tên nền tảng"/>
                </tree>
            </field>
        </record>

        <!-- PLATFORM Form View -->
        <record model="ir.ui.view" id="view_platform_form">
            <field name="name">platform.form</field>
            <field name="model">game.platform</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="Nền tảng">
                    <sheet>
                        <group col="2">
                            <field name="name" string="Tên nền tảng:"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- PLATFORM Action Window -->
        <record model="ir.actions.act_window" id="action_platform">
            <field name="name">Nền tảng</field>
            <field name="res_model">game.platform</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

        <!-- ============================================================================
             SERIES MODEL VIEWS
             ============================================================================ -->

        <!-- SERIES Search View -->
        <record model="ir.ui.view" id="view_series_search">
            <field name="name">series.search</field>
            <field name="model">game.series</field>
            <field name="type">search</field>
            <field name="arch" type="xml">
                <search string="Tìm kiếm Series">
                    <field name="name" string="Tên series"/>
                </search>
            </field>
        </record>

        <!-- SERIES Tree View -->
        <record model="ir.ui.view" id="view_series_tree">
            <field name="name">series.tree</field>
            <field name="model">game.series</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree string="Danh sách series">
                    <field name="name"/>
                </tree>
            </field>
        </record>

        <!-- SERIES Form View -->
        <record model="ir.ui.view" id="view_series_form">
            <field name="name">series.form</field>
            <field name="model">game.series</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="Game Series">
                    <sheet>
                        <group col="2" string="Thông tin series">
                            <field name="name" string="Tên series:" colspan="2"/>
                        </group>
                        <notebook>
                            <page string="Mô tả">
                                <field name="description" nolabel="1"/>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- SERIES Action Window -->
        <record model="ir.actions.act_window" id="action_series">
            <field name="name">Series</field>
            <field name="res_model">game.series</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
        </record>

    </data>
</openerp>
