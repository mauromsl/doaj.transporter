from marshmallow import Schema, fields, post_load, EXCLUDE

from doaj import data_structs

class StructSchema(Schema):
    _STRUCT_CLS = None

    @post_load
    def populate_struct(self, data, *args, **kwargs):
        if self._STRUCT_CLS:
            return self._STRUCT_CLS(**data)
        return data


class LicenseSchema(StructSchema):
    _STRUCT_CLS = data_structs.LicenseStruct
    open_access = fields.Boolean(default=True)
    title = fields.String()
    url = fields.URL()
    version = fields.String()
    type = fields.String()


class JournalSchema(StructSchema):
    _STRUCT_CLS = data_structs.JournalStruct
    country = fields.String()
    language = fields.List(fields.String())
    license = fields.List(fields.Nested(LicenseSchema))
    number = fields.String()
    volume = fields.String()
    publisher = fields.String()
    title = fields.String(required=True)
    start_page = fields.String()
    end_page = fields.String()


class IdentifierSchema(StructSchema):
    _STRUCT_CLS = data_structs.IdentifierStruct
    type = fields.String()
    id = fields.String()


class LinkSchema(StructSchema):
    _STRUCT_CLS = data_structs.LinkStruct
    content_type = fields.String()
    type = fields.String(default="fulltext")
    url = fields.URL()


class AuthorSchema(StructSchema):
    _STRUCT_CLS = data_structs.AuthorStruct
    name = fields.String()
    affiliation = fields.String()


class SubjectSchema(StructSchema):
    _STRUCT_CLS = data_structs.SubjectStruct
    code = fields.String()
    scheme = fields.String()
    term = fields.String()


class BibjsonSchema(StructSchema):
    _STRUCT_CLS = data_structs.BibjsonStruct

    abstract = fields.String()
    author = fields.List(fields.Nested(AuthorSchema))
    title = fields.String()
    year = fields.Int()
    month = fields.Int()
    identifier = fields.List(fields.Nested(IdentifierSchema))
    journal = fields.Nested(JournalSchema)
    keywords = fields.List(fields.String)
    link = fields.List(fields.Nested(LinkSchema))
    subject = fields.List(fields.Nested(SubjectSchema))


class AdminSchema(StructSchema):
    _STRUCT_CLS = data_structs.AdminStruct

    in_doaj = fields.Boolean(load_only=True)
    publisher_record_id = fields.String()
    upload_id = fields.String(load_only=True)
    seal = fields.Bool(load_only=True)


class ArticleSchema(Schema):
    admin = fields.Nested(AdminSchema)
    bibjson = fields.Nested(BibjsonSchema)
    created_date = fields.DateTime(format="iso", load_only=True)
    id = fields.String(load_only=True)
    last_updated = fields.DateTime(format="iso", load_only=True)

class SearchResultSchema(StructSchema):
    class Meta:
        unknown = EXCLUDE

    _STRUCT_CLS = data_structs.SearchResultStruct

    id = fields.String(required=True)
    last_updated = fields.DateTime(format="iso", load_only=True)
    created_date = fields.DateTime(format="iso", load_only=True)


class SearchSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    results = fields.List(fields.Nested(SearchResultSchema))

