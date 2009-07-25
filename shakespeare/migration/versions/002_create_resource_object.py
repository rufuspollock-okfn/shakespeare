from sqlalchemy import *
from migrate import *
import migrate.changeset
from shakespeare.migration.util import wrap_in_transaction

metadata = MetaData(migrate_engine)

material = Table('material', metadata, autoload=True)
src_pkg = Column('src_pkg', UnicodeText)
src_locator = Column('src_locator', UnicodeText)

resource_table = Table('resource', metadata,
    Column('id', Integer, primary_key=True),
    Column('material_id', Integer, ForeignKey('material.id')),
    Column('format', UnicodeText),
    # url or path
    Column('locator', UnicodeText),
    # types: url, cache, package, disk
    Column('locator_type', UnicodeText, default=u'url'),
    )

@wrap_in_transaction
def upgrade():
    resource_table.create()
    # TODO: ? migrate data
    material.c['src_pkg'].drop()
    material.c['src_locator'].drop()

@wrap_in_transaction
def downgrade():
    src_pkg.create(material)
    src_locator.create(material)
    # TODO: ? migrate data
    resource_table.drop()

