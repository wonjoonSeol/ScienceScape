import unittest
import sys
import os

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

from parse_and_group import is_year_within_span
from parse_and_group import create_span_files
from parse_and_group import separate_years
from parse_and_group import get_span_parameters

class TestParseGroup(unittest.TestCase):

    """
    This test tests that the method is_year_within_span works correctly
    for years in the span.
    """
    def test_year_within_span_true(self):
        allTrue = True
        for year in range(1990, 2010):
            if not is_year_within_span(1990, 2010, year):
                allTrue = False
        self.assertEqual(True, allTrue)

    """
    This test tests that the method is_year_within_span works correctly
    for years NOT in the span.
    """
    def test_year_within_span_false(self):
        allFalse = True
        for year in range(1900, 1989):
            if is_year_within_span(1990, 2010, year):
                allFalse = False
        self.assertEqual(True, allFalse)

    """
    This test tests that upon calling separate_years, the lines are correctly separated
    amongst the span files.
    """
    def test_years_correctly_separated(self):

        # Set up test folders/files (will be removed at the end of test)
        wos_headers = "PT	AU	BA	BE	GP	AF	BF	CA	TI	SO	SE	BS	LA	DT	CT	CY	CL	SP	HO	DE	ID	AB	C1	RP	EM	RI	OI	FU	FX	CR	NR	TC	Z9	U1	U2	PU	PI	PA	SN	EI	BN	J9	JI	PD	PY	VL	IS	PN	SU	SI	MA	BP	EP	AR	DI	D2	EA	EY	PG	WC	SC	GA	UT	PM	OA	HC	HP	DA"
        dir = os.path.dirname(os.path.dirname(__file__))
        os.makedirs(os.path.join(dir, "testFiles/foldersForSeparateYears"))
        os.makedirs(os.path.join(dir, "testFiles/foldersForSeparateYears/firstSpan"))
        os.makedirs(os.path.join(dir, "testFiles/foldersForSeparateYears/secondSpan"))
        first_span_txt = open(os.path.join(dir, "testFiles/foldersForSeparateYears/firstSpan/firstSpan.txt"), "w")
        second_span_txt = open(os.path.join(dir, "testFiles/foldersForSeparateYears/secondSpan/secondSpan.txt"), "w")
        first_span_txt.write(wos_headers + "\n")
        second_span_txt.write(wos_headers + "\n")

        # This is a dummy line for testing

        line = """J	Piersanti, S; Orlandi, A				Piersanti, Stefano; Orlandi, Antonio			Genetic Algorithm Optimization for the Total Radiated Power of a Meandered Line by Using an Artificial Neural Network	IEEE TRANSACTIONS ON ELECTROMAGNETIC COMPATIBILITY			English	Article						Artificial neural network (ANN); electromagnetic (EM) radiation; genetic algorithms (GAs); machine learning; meandered line; nature-inspired algorithms; signal integrity; total radiated power (TRP)		One of the state-of-the-art optimization strategies is the introduction of an artificial neural network in place of a more time-consuming numerical tool to compute the cost function. This work describes the development of a genetic algorithm optimization strategy for a meandered microstrip line by using an artificial neural network whose training set has been designed by a uniform sampling of the global design space. The results in terms of the total radiated electromagnetic power are discussed and compared with those obtained by the initial and not optimized configuration.	[Piersanti, Stefano; Orlandi, Antonio] Univ Aquila, Dept Ind & Informat Engn & Econ, UAq EMC Lab, I-67100 Laquila, Italy	Orlandi, A (reprint author), Univ Aquila, Dept Ind & Informat Engn & Econ, UAq EMC Lab, I-67100 Laquila, Italy.	stefano.piersanti@graduate.univaq.it; anto-nio.orlandi@univaq.it					Computer Simulation Technology, 2017, CST STUD SUIT 2017; Cuthbert T. R., 1987, OPTIMIZATION USING P; Duffy AP, 2006, IEEE T ELECTROMAGN C, V48, P449, DOI 10.1109/TEMC.2006.879358; HAGAN MT, 1994, IEEE T NEURAL NETWOR, V5, P989, DOI 10.1109/72.329697; Hagan M. T., 1995, NEURAL NETWORK DESIG; Hall S. H., 2009, ADV SIGNAL INTEGRITY; Haupt R.L., 2004, PRACTICAL GENETIC AL; [Anonymous], 2008, P1597 IEEE; Orlandi A., 2017, ELECTROMAGNETIC BAND; Orlandi A, 2006, IEEE T ELECTROMAGN C, V48, P460, DOI 10.1109/TEMC.2006.879360; Qi Q, 2016, EL PACKAG TECH CONF, P85, DOI 10.1109/EPTC.2016.7861448; Tron S., 2013, MEANDERED TRANSMISSI; Uka S., 1990, IEEE T NEURAL NETWOR, V2, P675	13	0	0	0	0	IEEE-INST ELECTRICAL ELECTRONICS ENGINEERS INC	PISCATAWAY	445 HOES LANE, PISCATAWAY, NJ 08855-4141 USA	0018-9375	1558-187X		IEEE T ELECTROMAGN C	IEEE Trans. Electromagn. Compat.	AUG	2018	60	4					1014	1017		10.1109/TEMC.2017.2764623				4	Engineering, Electrical & Electronic; Telecommunications	Engineering; Telecommunications	FT4JY	WOS:000423122600025					2018-02-07"""

        # Mocking some time spans
        spans = {
    			"firstSpan":{
    				"years":[1900,1999],
    			},
    			"secondSpan":{
    				"years":[2000, 2018],
    			}
    	}

        # Mocking a folder structure with dummy input/output files/folders
        years_spans = dict((s, data["years"]) for s, data in spans.items())

        files = {
            "firstSpan": first_span_txt,
            "secondSpan": second_span_txt,
        }

        # Call to the method we want to test
        separate_years(line, years_spans, files, 44)

        first_span_txt.close()
        second_span_txt.close()
        first_span_read = open(os.path.join(dir, "testFiles/foldersForSeparateYears/firstSpan/firstSpan.txt"), "r")
        second_span_read = open(os.path.join(dir, "testFiles/foldersForSeparateYears/secondSpan/secondSpan.txt"), "r")
        first_span_read.readline()
        second_span_read.readline()

        # Check that the years have been correctly separated
        result = False
        if len(first_span_read.readlines()) == 0 and len(second_span_read.readlines()) == 1:
            result = True

        # Tear down
        first_span_read.close()
        second_span_read.close()
        os.remove(os.path.join(dir, "testFiles/foldersForSeparateYears/firstSpan/firstSpan.txt"))
        os.remove(os.path.join(dir, "testFiles/foldersForSeparateYears/secondSpan/secondSpan.txt"))
        os.rmdir(os.path.join(dir, "testFiles/foldersForSeparateYears/firstSpan"))
        os.rmdir(os.path.join(dir, "testFiles/foldersForSeparateYears/secondSpan"))
        os.rmdir(os.path.join(dir, "testFiles/foldersForSeparateYears"))

        self.assertEqual(True, result)

    def test_get_span_parameters(self):
        mocked_spans = {
            "first_span":{
                "years":[1789,2010]
            },
            "second_span":{
                "years":[2011,2018]
            },
        }
        result = str(get_span_parameters(mocked_spans.items(), "years"))
        self.assertEqual(result, """{'first_span': [1789, 2010], 'second_span': [2011, 2018]}""")

if __name__ == '__main__':
    unittest.main()
