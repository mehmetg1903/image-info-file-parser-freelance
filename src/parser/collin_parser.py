from xml.dom import minidom

from ..util.string_helper import remove_multiple_spaces


class CollinParser:

    def __init__(self, file_name):
        self._dom = minidom.parse(file_name)

    @staticmethod
    def _get_data_from_element(element, tag):
        tag_node = element.getElementsByTagName(tag)
        if tag_node[0].firstChild is not None:
            return tag_node[0].firstChild.data
        return ""

    def parse(self, db):
        inserted = 0
        for doc in self._dom.getElementsByTagName("DOCUMENT"):
            try:
                seq_key = remove_multiple_spaces(CollinParser._get_data_from_element(doc, "SEQ_KEY"))
                recevice_date = remove_multiple_spaces(CollinParser._get_data_from_element(doc, "RECDATE1"))
                business_node = doc.getElementsByTagName("ENTITY")[0]
                business_name = CollinParser._get_data_from_element(business_node, "LNAME")
                zip = CollinParser._get_data_from_element(business_node, "ZIP")

                owner_name, owner_city, owner_addr, owner_state = "", "", "", ""

                owner_nodes = doc.getElementsByTagName("ENTITY")[1:]
                for owner_node in owner_nodes:
                    owner_name = CollinParser._get_data_from_element(owner_node, "FNAME") + " " + \
                                 CollinParser._get_data_from_element(owner_node, "LNAME")

                    owner_addr = CollinParser._get_data_from_element(owner_node, "ADDRESS1") + " " + \
                                 CollinParser._get_data_from_element(owner_node, "ADDRESS2")

                    owner_city = CollinParser._get_data_from_element(owner_node, "CITY")
                    owner_state = CollinParser._get_data_from_element(owner_node, "STATE")

                args = (seq_key,
                        recevice_date,
                        business_name,
                        owner_name,
                        owner_addr,
                        owner_city,
                        owner_state,
                        zip)

                db.run_insert_query(args)
                inserted = inserted + 1
            except:
                pass

        print("There are {} rows inserted".format(inserted))
