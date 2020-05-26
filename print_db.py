from __future__ import division
from sqlalchemy import create_engine, MetaData, inspect, Table
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':

    engine = create_engine('sqlite:///GP.db')  # Change "lecture.db" to whatever your .db file's name is.

    metadata = MetaData(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    table_names = inspect(engine).get_table_names()

    table_strings = []
    for table_name in table_names:
        table_string = '\n'
        table = Table(table_name, metadata, autoload=True)

        columns = [str(c).split('.')[-1] for c in table.columns]

        table_to_print = session.query(table).all()

        max_lengths = []

        # If there are no rows, we still want to print the headers
        if len(table_to_print) == 0:
            max_lengths = [len(c) + 2 for c in columns]
        else:
            for title, data in zip(columns, zip(*table_to_print)):
                max_lengths.append(max([len(repr(d)) for d in data + (title,)]) + 2)
        row_format = ''.join(["{:>%d}" % length for length in max_lengths])

        header = row_format.format(*columns)
        width = len(header)
        title_pad = (width - len(table_name)) // 2

        table_string += (' ' * title_pad + table_name + ' ' * title_pad)
        hline = '\n' + '-' * len(header) + '\n'
        table_string += hline + header + hline


        def make_row(row):
            try:
                row = [str(c) for c in row]
            except:
                row = ['None' if c is None else c for c in row]
            return row_format.format(*row)


        row_strings = '\n'.join([make_row(row) for row in table_to_print])

        table_string += row_strings

        table_strings.append(table_string)
    print('\n\n'.join(table_strings))
