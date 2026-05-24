# -*- coding: utf-8 -*-
from datetime import datetime
from openerp.osv import fields, osv

try:
    integer_types = (int, long)
except NameError:
    integer_types = (int,)


def _as_list(ids):
    if isinstance(ids, integer_types):
        return [ids]
    return list(ids)


def _has_model_reference(pool, cr, uid, model_name, field_name, ids, context=None):
    return bool(pool.get(model_name).search(
        cr,
        uid,
        [(field_name, 'in', _as_list(ids))],
        limit=1,
        context=context
    ))


def _has_relation_reference(cr, table_name, column_name, ids):
    cr.execute(
        'SELECT 1 FROM %s WHERE %s = ANY(%%s) LIMIT 1' % (table_name, column_name),
        (_as_list(ids),)
    )
    return bool(cr.fetchone())


def _raise_delete_restricted(record_name):
    raise osv.except_osv(
        u'Lỗi',
        u'Không thể xóa %s vì đang được sử dụng bởi dữ liệu khóa ngoại!' % record_name
    )

class Game(osv.osv):
    """
    GAME MODEL - Core entity for video game information

    Represents a single video game title with comprehensive metadata including
    release information, genre classification, pricing, and relationships to
    publisher, developer studio, and available platforms.
    """

    _name = 'game.game'
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_model_reference(self.pool, cr, uid, 'game.version', 'game_id', ids, context=context):
            _raise_delete_restricted(u'game')
        return super(Game, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
    # ('vals', {u'status': u'released', u'name': u'\u0111\xe0', u'release_date': u'2009-05-05 00:00:00', u'series_id': 1, u'platforms':
    # [[6, False, [1]]], u'notes': False, u'genre': u'rpg', u'studio_id': 1, u'publisher_id': 2, u'price': 1, u'description': False})
        print("vals", vals)

        if 'price' in vals:
            print("price", vals['price'])
            if vals['price'] <= 0:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Giá game phải lớn hơn 0!'
                )

        if 'release_date' in vals:
            if vals['release_date'] is False:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Ngày phát hành không được để trống!'
            )
            print("release_date", vals['release_date'])
            print("datetime.now()", datetime.now())
            release_date = datetime.strptime(vals['release_date'], '%Y-%m-%d %H:%M:%S')
            if release_date <= datetime.now():
                raise osv.except_osv(
                    u'Lỗi',
                    u'Ngày phát hành không được trước hoặc trùng với ngày hiện tại!'
            )

        if 'publisher_id' not in vals:
            raise osv.except_osv(
                u'Lỗi',
                u'Nhà phát hành không được để trống!'
            )

        if 'studio_id' not in vals:
            raise osv.except_osv(
                u'Lỗi',
                u'Studio phát triển game không được để trống!'
            )

        if 'release_date' not in vals:
            raise osv.except_osv(
                u'Lỗi',
                u'Ngày phát hành không được để trống!'
            )


        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên game không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên game đã tồn tại!'
                )

        return super(Game, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        print("vals in write", vals)
        # if 'publisher_id' not in vals:
        #     raise osv.except_osv(
        #         u'Lỗi',
        #         u'Nhà phát hành không được để trống!'
        #     )

        # if 'studio_id' not in vals:
        #     raise osv.except_osv(
        #         u'Lỗi',
        #         u'Studio phát triển game không được để trống!'
        #     )
        if 'release_date' in vals:
            print("release_date", vals['release_date'])
            print("datetime.now()", datetime.now())
            release_date = datetime.strptime(vals['release_date'], '%Y-%m-%d %H:%M:%S')
            if release_date <= datetime.now():
                raise osv.except_osv(
                    u'Lỗi',
                    u'Ngày phát hành không được trước hoặc trùng với ngày hiện tại!'
            )

        if 'price' in vals:
            print("price", vals['price'])
            if vals['price'] <= 0:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Giá game phải lớn hơn 0!'
                )

        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên game không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [
                    ('name', '=', vals['name']),
                    ('id', 'not in', ids)
                ],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên game đã tồn tại!'
                )

        return super(Game, self).write(cr, uid, ids, vals, context=context)

    def _get_genres_display(self, cr, uid, ids, field_name, arg, context=None):
        """
        This method returns the display name of the genres for the given record.
        It is used to display the genres's name in the tree view and form view.
        """
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        print("id's: ",records)
        for game in records:
            print("id's: ",game)
            print("game.genres: ",game.genres)
            # print("game.genres.name: ",game.genres.name)
            if game.genres:
                result[game.id] = ", ".join([g.name for g in game.genres])
            else:
                result[game.id] = 'Chưa có thông tin về thể loại game'

        return result

    def _get_publisher_display(self, cr, uid, ids, field_name, arg, context=None):
        """
        This method returns the display name of the publisher for the given record.
        It is used to display the publisher's name in the tree view and form view.
        """
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        print("id's: ",records)
        for game in records:
            print("id's: ",game)
            print("game: ",game.publisher_id)
            print("game: ",game.publisher_id.name)
            if game.publisher_id:
                result[game.id] = game.publisher_id.name
            else:
                result[game.id] = 'Chưa có thông tin về nhà phát hành'

        return result

    def _get_studio_display(self, cr, uid, ids, field_name, arg, context=None):
        """
        This method returns the display name of the studio for the given record.
        It is used to display the studio's name in the tree view and form view.
        """
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        print("id's: ",records)
        for game in records:
            print("id's: ",game)
            print("game: ",game.studio_id)
            print("game: ",game.studio_id.name)
            if game.studio_id:
                result[game.id] = game.studio_id.name
            else:
                result[game.id] = 'Chưa có thông tin về studio phát triển game'

        return result

    def _version_tuple(self, version):
        return tuple(map(int, version.split('.')))

    def _has_update(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        version_obj = self.pool.get('game.version')
        for game in self.browse(cr, uid, ids, context=context):
            result[game.id] = False
            version_ids = version_obj.search(
                cr,
                uid,
                [('game_id', '=', game.id)],
                order='version_name desc',
                limit=1
            )

            if not version_ids:
                continue

            latest_version = version_obj.browse(
                cr,
                uid,
                version_ids[0],
                context=context
            )
            if not game.current_version:
                result[game.id] = True
                continue

            current = self._version_tuple(game.current_version)
            latest = self._version_tuple(latest_version.version_name)

            if current < latest:
                result[game.id] = True

        return result

    def _get_latest_version_display(self, cr, uid, ids, field_name, arg, context=None):

        result = {}

        version_obj = self.pool.get('game.version')

        for game in self.browse(cr, uid, ids, context=context):

            version_ids = version_obj.search(
                cr,
                uid,
                [('game_id', '=', game.id)],
                order='version_name desc',
                limit=1
            )

            if not version_ids:
                result[game.id] = u'Chưa có phiên bản'
                continue

            latest_version = version_obj.browse(
                cr,
                uid,
                version_ids[0],
                context=context
            )

            if game.has_update:
                result[game.id] = u'Có bản cập nhật %s' % latest_version.version_name
            else:
                result[game.id] = u'Đã cập nhật bản mới nhất'

        return result

    def action_update_game(self, cr, uid, ids, context=None):

        game = self.browse(cr, uid, ids[0], context=context)

        version_obj = self.pool.get('game.version')

        version_ids = version_obj.search(
            cr,
            uid,
            [('game_id', '=', game.id)],
            order='version_name desc',
            limit=1
        )

        if version_ids:

            latest_version = version_obj.browse(
                cr,
                uid,
                version_ids[0],
                context=context
            )

            self.write(
                cr,
                uid,
                ids,
                {
                    'current_version': latest_version.version_name
                },
                context=context
            )

        return True

    _columns = {

        'name': fields.char(
            'Tên game',
            size=25,
            required=True,
        ),
        'description': fields.text('Mô tả'),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),
        'release_date': fields.datetime('Ngày phát hành'),
        'status': fields.selection([
            ('released', 'Đã phát hành'),
            ('upcoming', 'Sắp phát hành'),
            ('cancelled', 'Đã hủy')
        ], 'Trạng thái', required=True),

        'notes': fields.text('Chi tiết'),

        'price': fields.float('Giá'),

        'publisher_id': fields.many2one(
            'game.publisher',
            'Nhà phát hành'
        ),
        'version_id': fields.one2many(
            'game.version',
            'game_id',
            'Phiên bản'
        ),
        'genres': fields.many2many(
            'game.genre',
            'game_genre_rel',
            'game_id',
            'genre_id',
            'Thể loại',
            required=True
            ),

        'studio_id': fields.many2one(
            'game.studio',
            'Studio phát triển game'
        ),

        'series_id': fields.many2one(
            'game.series',
            'Series'
        ),

        'platforms': fields.many2many(
            'game.platform',
            'game_platform_rel',
            'game_id',
            'platform_id',
            'Nền tảng',
            required=True
        ),


        'display_name':fields.function(
        _get_publisher_display
        ,type='char'
        ,string='Tên nhà phát hành'
        ),
        'display_studio_name':fields.function(
        _get_studio_display
        ,type='char'
        ,string='Tên Studio'
        ),
        'display_genres_name':fields.function(
        _get_genres_display
        ,type='char'
        ,string='Tên Thể Loại'
        ),
        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),

        'current_version': fields.char(
            'Phiên bản hiện tại',
            size=20
        ),

        'has_update': fields.function(
            _has_update,
            type='boolean',
            string='Có bản cập nhật'
        ),

        'latest_version_display': fields.function(
            _get_latest_version_display,
            type='char',
            string='Trạng thái cập nhật'
        ),
    }


class Publisher(osv.osv):
    """
    PUBLISHER MODEL
    One publisher can distribute multiple games (one2many relationship).
    """

    _name = 'game.publisher'
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_model_reference(self.pool, cr, uid, 'game.game', 'publisher_id', ids, context=context):
            _raise_delete_restricted(u'nhà phát hành')
        return super(Publisher, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhà phát hành không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhà phát hành đã tồn tại!'
                )
        return super(Publisher, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhà phát hành không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhà phát hành đã tồn tại!'
                )
        return super(Publisher, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'name': fields.char(
            'Tên nhà phát hành',
            size=25,
            required=True
        ),

        'country': fields.char(
            'Quốc gia',
            size=25,
            required=True
        ),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),

    }


class Studio(osv.osv):
    """
    STUDIO MODEL - Manages development studios

    A studio is a company that develops (creates) games.
    One studio can develop multiple games and employ multiple members.
    """

    _name = 'game.studio'
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_model_reference(self.pool, cr, uid, 'game.game', 'studio_id', ids, context=context):
            _raise_delete_restricted(u'studio')
        if _has_relation_reference(cr, 'game_studio_member_rel', 'studio_id', ids):
            _raise_delete_restricted(u'studio')
        return super(Studio, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Studio phát triển game không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Studio phát triển game đã tồn tại!'
                )
        return super(Studio, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Studio phát triển game không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Studio phát triển game đã tồn tại!'
                )
        return super(Studio, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'name': fields.char(
            'Tên studio phát triển game',
            size=25,
            required=True
        ),

        'headquarter': fields.char(
            'Trụ sở chính',
            size=25,
            required=True
        ),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),

        'members': fields.many2many(
            'game.member',
            'game_studio_member_rel',
            'studio_id',
            'member_id',
            'Nhân viên',
            required=True
        ),

    }

class Member(osv.osv):
    """
    MEMBER MODEL - Manages development team members

    Represents an employee working at a game development studio.
    Each member belongs to exactly ONE studio.

    A Member must be associated with a Studio

    """

    _name = 'game.member'  # Database table: game_member
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_relation_reference(cr, 'game_studio_member_rel', 'member_id', ids):
            _raise_delete_restricted(u'nhân viên')
        if _has_relation_reference(cr, 'game_member_role_rel', 'member_id', ids):
            _raise_delete_restricted(u'nhân viên')
        return super(Member, self).unlink(cr, uid, ids, context=context)

    def _get_studios_display(self, cr, uid, ids, field_name, arg, context=None):
        """
        This method returns the display name of the studios for the given record.
        It is used to display the studios's name in the tree view and form view.
        """
        result = {}
        records = self.browse(cr, uid, ids, context=context)
        print("id's: ",records)
        for member in records:
            print("id's: ",member)
            print("member.studios: ",member.studios)
            # print("member.studios.name: ",member.studios.name)
            if member.studios:
                result[member.id] = ", ".join([s.name for s in member.studios])
            else:
                result[member.id] = 'Chưa có thông tin về studio phát triển game'

        return result

    def create(self, cr, uid, vals, context=None):
    # ('vals', {u'status': u'released', u'name': u'\u0111\xe0', u'release_date': u'2009-05-05 00:00:00', u'series_id': 1, u'platforms':
    # [[6, False, [1]]], u'notes': False, u'genre': u'rpg', u'studio_id': 1, u'publisher_id': 2, u'price': 1, u'description': False})
        print("vals", vals)

        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhân viên không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhân viên đã tồn tại!'
                )

        return super(Member, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhân viên không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên Nhân viên đã tồn tại!'
                )
        return super(Member, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'name': fields.char(
            'Tên nhân viên',
            size=25,
            required=True
        ),
        # Employee's full name
        # Example: 'Adam Badowski', 'Naoki Yoshida', 'Neil Druckmann'

        'studios': fields.many2many(
            'game.studio',
            'game_studio_member_rel',
            'member_id',
            'studio_id',
            'Studio',
        ),

        'roles': fields.many2many(
            'game.role',
            'game_member_role_rel',
            'member_id',
            'role_id',
            'Chức vụ',
            required=True
        ),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),
        'display_studios_name': fields.function(
            _get_studios_display,
            type='char',
            string='Studio phát triển game',
            store=False
        ),


    }


class Genre(osv.osv):
    """
    GENRE MODEL - Manages game genre categories

    Represents a game genre/category that can be assigned to games.
    This is a reference table for genre definitions.
    """

    _name = 'game.genre'
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_relation_reference(cr, 'game_genre_rel', 'genre_id', ids):
            _raise_delete_restricted(u'thể loại')
        return super(Genre, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên thể loại không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên thể loại đã tồn tại!'
                )
        return super(Genre, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên thể loại không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên thể loại đã tồn tại!'
                )
        return super(Genre, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'name': fields.char(
            'Tên thể loại',
            size=25,
            required=True
        ),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),

    }


class Platform(osv.osv):
    """
    PLATFORM MODEL - Manages gaming platforms/systems

    Represents a gaming platform/system where games can be played.
    Games link to platforms via many2many relationship.
    """

    _name = 'game.platform'
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_relation_reference(cr, 'game_platform_rel', 'platform_id', ids):
            _raise_delete_restricted(u'nền tảng')
        return super(Platform, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên máy tính không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên máy tính đã tồn tại!'
                )
        return super(Platform, self).create(cr, uid, vals, context=context)

    def write(self,cr,uid,ids,vals,context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên máy tính không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên máy tính đã tồn tại!'
                )
        return super(Platform, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'name': fields.char(
            'Tên máy tính',
            size=25,
            required=True
        ),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),

    }


class Series(osv.osv):
    """
    SERIES MODEL - Manages game series/franchises

    Represents a game series/franchise that can contain multiple game titles.
    One series can have many games (one2many relationship with Game model).
    """

    _name = 'game.series'
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_model_reference(self.pool, cr, uid, 'game.game', 'series_id', ids, context=context):
            _raise_delete_restricted(u'series')
        return super(Series, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên series không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên series đã tồn tại!'
                )
        return super(Series, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên series không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên series đã tồn tại!'
                )
        return super(Series, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'name': fields.char(
            'Tên series',
            size=25,
            required=True
        ),

        'description': fields.text('Mô tả'),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),
    }


class Role(osv.osv):
    _name = 'game.role'
    _log_access = True

    def unlink(self, cr, uid, ids, context=None):
        if _has_relation_reference(cr, 'game_member_role_rel', 'role_id', ids):
            _raise_delete_restricted(u'vai trò')
        return super(Role, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên vai trò không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên vai trò đã tồn tại!'
                )
        return super(Role, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'name' in vals:
            vals['name'] = vals['name'].strip()
            if vals['name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên vai trò không được để trống!'
                )
            existing = self.search(
                cr,
                uid,
                [('name', '=', vals['name'])],
                context=context
            )
            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên vai trò đã tồn tại!'
                )

        return super(Role, self).write(cr, uid, ids, vals, context=context)

    _columns = {
        'name': fields.char(
            'Tên vai trò',
            size=25,
            required=True
        ),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),

    }

import re

class GameVersion(osv.osv):

    _name = 'game.version'

    def create(self, cr, uid, vals, context=None):

        if 'version_name' in vals:

            vals['version_name'] = vals['version_name'].strip()

            if vals['version_name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên phiên bản không được để trống!'
                )

            if not re.match(r'^\d+(\.\d+)*$', vals['version_name']):
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên phiên bản phải là số và không chứa ký tự đặc biệt!'
                )

            existing = self.search(
                cr,
                uid,
                [
                    ('version_name', '=', vals['version_name']),
                    ('game_id', '=', vals.get('game_id'))
                ],
                context=context
            )

            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên phiên bản đã tồn tại!'
                )

        return super(GameVersion, self).create(
            cr,
            uid,
            vals,
            context=context
        )

    def write(self, cr, uid, ids, vals, context=None):

        if 'version_name' in vals:

            vals['version_name'] = vals['version_name'].strip()

            if vals['version_name'] == '':
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên phiên bản không được để trống!'
                )

            if not re.match(r'^\d+(\.\d+)*$', vals['version_name']):
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên phiên bản phải là số và không chứa ký tự đặc biệt!'
                )

            game_id = vals.get('game_id')

            if not game_id:
                current_version = self.browse(
                    cr,
                    uid,
                    ids[0],
                    context=context
                )

                game_id = current_version.game_id.id

            existing = self.search(
                cr,
                uid,
                [
                    ('version_name', '=', vals['version_name']),
                    ('game_id', '=', game_id),
                    ('id', 'not in', ids)
                ],
                context=context
            )

            if existing:
                raise osv.except_osv(
                    u'Lỗi',
                    u'Tên phiên bản đã tồn tại!'
                )

        return super(GameVersion, self).write(
            cr,
            uid,
            ids,
            vals,
            context=context
        )

    _columns = {

        'version_name': fields.char(
            'Phiên bản',
            size=20,
            required=True
        ),

        'enhancement_notes': fields.text(
            'Nội dung cập nhật',
            required=True
        ),

        'game_id': fields.many2one(
            'game.game',
            'Game',
            ondelete='cascade'
        ),

        'create_date': fields.datetime(
            'Ngày Tạo',
            readonly=True
        ),

        'write_date': fields.datetime(
            'Ngày cập nhật',
            readonly=True
        ),
    }
