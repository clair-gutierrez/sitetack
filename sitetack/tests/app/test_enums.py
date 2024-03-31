from sitetack.app.enums import PtmKind, OrganismKind, LabelKind, kind_to_dict



class TestEnums:


    def test_kind_to_dict_labels_has_correct_element(self):
        d = kind_to_dict(LabelKind)
        assert d["NO_LABELS"] == {
            "name": "No Labels",
            "filename_query": "no_labels",
            "description": "No labels does not encode known PTM locations.",
        }
    
    def test_kind_to_dict_organisms_has_correct_element(self):
        d = kind_to_dict(OrganismKind)
        assert d["HUMAN"] == {
            "name": "Human",
            "directory_name": "Human",
            "description": "Model trained on only human proteins",
        }

    def test_kind_to_dict_ptms_has_correct_element(self):
        d = kind_to_dict(PtmKind)
        print(f"d: {d}")
        assert d["HYDROXYLYSINE_K"] == {
            "name": "Hydroxylysine (K)",
            "amino_acids": ["K"],
            "description": "Hydroxylysine is a derivative of the amino acid lysine, which is used to form cross-links in collagen.",
            'directory_name': 'Hydroxylysine (K)',
        }
