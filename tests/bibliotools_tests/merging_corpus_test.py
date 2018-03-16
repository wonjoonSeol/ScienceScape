import unittest
import sys
import os

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

from merging_corpus import count_occurences
from merging_corpus import write_to_file
from merging_corpus import number_columns
from merging_corpus import parse_line
from merging_corpus import write_report
from merging_corpus import prepare_output_file
from merging_corpus import prepare_report_directory
from merging_corpus import prepare_error_file

class TestMergingCorpus(unittest.TestCase):

    """
    This test tests that upon calling count_occurrences,
    a report file is created in the given directory to report year information.
    """
    def test_count_occurrences_and_write_year_distrib_yield_csv_file(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        count_occurences(os.path.join(dir, "testFiles/test.txt"), os.path.join(dir, "testFiles"))
        years_distrib_found = False

        for file in os.listdir(os.path.join(dir, "testFiles")):
            if file.endswith('years_distribution.csv'):
                years_distrib_found = True
                os.remove(os.path.join(dir, "testFiles/years_distribution.csv"))
        self.assertEqual(True,years_distrib_found)

    """
    This test tests that upon calling count_occurrences with an empty source file,
    the years_distribution.csv file is empty, but still contains the header.
    """
    def test_count_occurrences_yields_blank_file_for_empty_source(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        count_occurences(os.path.join(dir, "testFiles/test.txt"), os.path.join(dir, "testFiles"))
        emptyFile = False

        for file in os.listdir(os.path.join(dir, "testFiles")):
            if file.endswith('years_distribution.csv'):
                years_distribution = open(os.path.join(dir, "testFiles/years_distribution.csv"), "r")
                years_distribution.readline()   # We remove the header

                if len(years_distribution.readlines()) == 0:
                    emptyFile = True

                os.remove(os.path.join(dir, "testFiles/years_distribution.csv"))
        self.assertEqual(True,emptyFile)

    """
    This test tests that write_to_file(...) writes correctly to a file without corrupting the
    text to write.
    """
    def test_write_to_file(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_write_to = open(os.path.join(dir, "testFiles/dummyfile.txt"), "w")
        text_to_write = "firstline\nsecondline\nthirdline"
        write_to_file(file_to_write_to, text_to_write)
        file_to_write_to.close()
        file_to_read = open(os.path.join(dir, "testFiles/dummyfile.txt"), "r")
        lines_read = file_to_read.readlines()
        file_to_read.close()
        os.remove(os.path.join(dir, "testFiles/dummyfile.txt"))
        result = False
        if lines_read[0] == "firstline\n" and lines_read[1] == "secondline\n" and lines_read[2] == "thirdline":
            result = True
        self.assertEqual(True, result)

    """
    This test tests that the number of columns in a line can be correctly
    determined by the number_columns function.
    """
    def test_number_columns(self):
        line_to_test = "PT	AU	BA	BE	GP	AF	BF	CA	TI	SO	SE	BS	LA	DT	CT	CY	CL	SP	HO	DE	ID	AB	C1	RP	EM	RI	OI	FU	FX	CR	NR	TC	Z9	U1	U2	PU	PI	PA	SN	EI	BN	J9	JI	PD	PY	VL	IS	PN	SU	SI	MA	BP	EP	AR	DI	D2	EA	EY	PG	WC	SC	GA	UT	PM	OA	HC	HP	DA"
        self.assertEqual(True, number_columns(line_to_test) == 68)

    """
    This test tests that a valid WOS line can be parsed.
    """
    def test_parse_line_for_valid_line(self):
        line_to_parse = """J	Kanjo, E; Younis, EMG; Sherkat, N				Kanjo, Eiman; Younis, Eman M. G.; Sherkat, Nasser			Towards unravelling the relationship between on-body, environmental and emotion data using sensor information fusion approach	INFORMATION FUSION			English	Article						Multi sensor data fusion; Regression analysis sensor data; Multivariable regression; Affective computing; Physiological signals; Machine learning	AIR-POLLUTION; NOISE EXPOSURE; HUMAN MOBILITY; GLOBAL BURDEN; FRAMEWORK; NETWORK; DISEASE; QUALITY; SYSTEMS; MODELS	Over the past few years, there has been a noticeable advancement in environmental models and information fusion systems taking advantage of the recent developments in sensor and mobile technologies. However, little attention has been paid so far to quantifying the relationship between environment changes and their impact on our bodies in real-life settings. In this paper, we identify a data driven approach based on direct and continuous sensor data to assess the impact of the surrounding environment and physiological changes and emotion. We aim at investigating the potential of fusing on-body physiological signals, environmental sensory data and on-line self-report emotion measures in order to achieve the following objectives: (1) model the short term impact of the ambient environment on human body, (2) predict emotions based on-body sensors and environmental data. To achieve this, we have conducted a real-world study 'in the wild' with on-body and mobile sensors. Data was collected from participants walking around Nottingham city centre, in order to develop analytical and predictive models. Multiple regression, after allowing for possible confounders, showed a noticeable correlation between noise exposure and heart rate. Similarly, UV and environmental noise have been shown to have a noticeable effect on changes in ElectroDermal Activity (EDA). Air pressure demonstrated the greatest contribution towards the detected changes in body temperature and motion. Also, significant correlation was found between air pressure and heart rate. Finally, decision fusion of the classification results from different modalities is performed. To the best of our knowledge this work presents the first attempt at fusing and modelling data from environmental and physiological sources collected from sensors in a real-world setting. (C) 2017 The Authors. Published by Elsevier B.V.	[Kanjo, Eiman; Sherkat, Nasser] Nottingham Trent Univ, Comp & Technol, Nottingham, England; [Younis, Eman M. G.] Menia Univ, Fac Comp & Informat, Al Minya, Egypt	Kanjo, E (reprint author), Nottingham Trent Univ, Comp & Technol, Nottingham, England.	eiman.kanjo@ntu.ac.uk; eman.younas@mu.edu.eg; Nasser.Sherkat@ntu.ac.uk		Sherkat, Nasser/0000-0003-1488-5682; kanjo, eiman/0000-0002-1720-0661	B11 Research unit at NTU [3452]	This work was supported by the B11 Research unit at NTU, Ref 3452. Also, the authors would like to thank Dr. Caroline Langen-siepen for her help with the Ethical Approval Application and Dr. Ahmed Aldabbagh for his help in collecting the data.	Adibuzzaman M, 2013, APPL COMPUT REV, V13, P67, DOI 10.1145/2513228.2513290.; Alajmi N, 2013, INT CONF AFFECT, P745, DOI 10.1109/ACII.2013.138; Al-Barrak L., 2013, AUG HUM C, P186; Al-Husain L., 2013, SENSE SPACE MAPPING, P1321; Banzhaf E, 2014, ECOL INDIC, V45, P664, DOI 10.1016/j.ecolind.2014.06.002; Barabasi AL, 2005, NATURE, V435, P207, DOI 10.1038/nature03459; BRADLEY MM, 1994, J BEHAV THER EXP PSY, V25, P49, DOI 10.1016/0005-7916(94)90063-9; Briggs D, 2003, BRIT MED BULL, V68, P1, DOI 10.1093/bmb/ldg019; Chamberlain A, 2014, PERS UBIQUIT COMPUT, V18, P1775, DOI 10.1007/s00779-013-0756-x; Chen H., 2016, LANCET; Chen M, 2011, MOBILE NETW APPL, V16, P171, DOI 10.1007/s11036-010-0260-8; Chung WY, 2007, P ANN INT IEEE EMBS, P3818, DOI 10.1109/IEMBS.2007.4353164; Granero AC, 2016, FRONT COMPUT NEUROSC, V10, DOI 10.3389/fncom.2016.00074; Danet S., UNHEALTHY EFFECTS AT; Datcu D., 2009, DCI I 2009; de Nazelle A, 2013, ENVIRON POLLUT, V176, P92, DOI 10.1016/j.envpol.2012.12.032; DOCKERY DW, 1994, ANNU REV PUBL HEALTH, V15, P107, DOI 10.1146/annurev.pu.15.050194.000543; Engel-Cox J, 2013, ATMOS ENVIRON, V80, P584, DOI 10.1016/j.atmosenv.2013.08.016; Fortino G, 2013, IEEE T HUM-MACH SYST, V43, P115, DOI 10.1109/TSMCC.2012.2215852; Freund Y., 1999, Journal of Japanese Society for Artificial Intelligence, V14, P771; Galelli S, 2014, ENVIRON MODELL SOFTW, V62, P33, DOI 10.1016/j.envsoft.2014.08.015; Gravina R, 2017, INFORM FUSION, V35, P68, DOI 10.1016/j.inffus.2016.09.005; Gravina R, 2016, IEEE T AFFECT COMPUT, V7, P286, DOI 10.1109/TAFFC.2016.2515094; Gromping U, 2006, J STAT SOFTW, V17; Guendil Z, 2016, 2016 2ND INTERNATIONAL CONFERENCE ON ADVANCED TECHNOLOGIES FOR SIGNAL AND IMAGE PROCESSING (ATSIP), P793, DOI 10.1109/ATSIP.2016.7523190; Guthier B, 2016, LECT NOTES COMPUT SC, V9970, P402, DOI 10.1007/978-3-319-46152-6_16; Hardie W., 2007, APPL MULTIVARIATE ST, P22007; Hidalgo B, 2013, AM J PUBLIC HEALTH, V103, P39, DOI 10.2105/AJPH.2012.300897; Irrgang M, 2016, PLOS ONE, V11, DOI 10.1371/journal.pone.0154360; Kampa M, 2008, ENVIRON POLLUT, V151, P362, DOI 10.1016/j.envpol.2007.06.012; Kanjo E., 2017, PLOS ONE IN PRESS; Kanjo E, 2008, PERS UBIQUIT COMPUT, V12, P599, DOI 10.1007/s00779-007-0180-1; Kanjo E, 2015, PERS UBIQUIT COMPUT, V19, P1197, DOI 10.1007/s00779-015-0842-3; Kanjo E, 2009, IEEE PERVAS COMPUT, V8, P50, DOI 10.1109/MPRV.2009.79; Khandoker A.H., 2013, PINCARE PLOT METHODS; Kim J, 2008, IEEE T PATTERN ANAL, V30, P2067, DOI 10.1109/TPAMI.2008.26; Kim KH, 2004, MED BIOL ENG COMPUT, V42, P419, DOI 10.1007/BF02344719; Knapp RB, 2011, COGN TECHNOL, P133, DOI 10.1007/978-3-642-15184-2_9; Kraus U, 2013, ENVIRON HEALTH PERSP, V121, P607, DOI 10.1289/ehp.1205606; Kreibig SD, 2010, BIOL PSYCHOL, V84, P394, DOI 10.1016/j.biopsycho.2010.03.010; Lim SS, 2012, LANCET, V380, P2224, DOI 10.1016/S0140-6736(12)61766-8; Lim YH, 2012, ENVIRON HEALTH PERSP, V120, P1023, DOI 10.1289/ehp.1104100; Lisetti C.L., 2004, EURASIP J ADV SIG PR; Makivic B., 2015, ASPETAR SPORTS MED J, V4, P326; Marton ZC, 2013, PATTERN RECOGN LETT, V34, P754, DOI 10.1016/j.patrec.2012.07.011; Mawass N.E., 2013, SUPERMARKET STRESS M, P1043; Mots L., 2011, J INDIVIDUAL DIFFERE; Munzel T, 2014, EUR HEART J, V35, P829, DOI 10.1093/eurheartj/ehu030; Park N., 2007, J INTERIOR DES, V33, P17, DOI DOI 10.1111/J.1939-1668.2007.TB00419.X; Picard RW, 2001, IEEE T PATTERN ANAL, V23, P1175, DOI 10.1109/34.954607; Polikar R, 2012, ENSEMBLE MACHINE LEARNING: METHODS AND APPLICATIONS, P1, DOI 10.1007/978-1-4419-9326-7_1; Ramzan N., 2016, ELECT IMAG, V2016, P1; Reis S, 2015, ENVIRON MODELL SOFTW, V74, P238, DOI 10.1016/j.envsoft.2015.06.003; Schlink U, 2010, SCI TOTAL ENVIRON, V408, P3918, DOI 10.1016/j.scitotenv.2010.03.018; Stansfeld S, 2000, Rev Environ Health, V15, P43; Steinle S, 2015, SCI TOTAL ENVIRON, V508, P383, DOI 10.1016/j.scitotenv.2014.12.003; Steinle S, 2013, SCI TOTAL ENVIRON, V443, P184, DOI 10.1016/j.scitotenv.2012.10.098; Takahashi K, 2004, RO-MAN 2004: 13TH IEEE INTERNATIONAL WORKSHOP ON ROBOT AND HUMAN INTERACTIVE COMMUNICATION, PROCEEDINGS, P95, DOI 10.1109/ROMAN.2004.1374736; Valstar M., 2016, ARXIV160501600; van Kempen EEMM, 2002, ENVIRON HEALTH PERSP, V110, P307, DOI 10.1289/ehp.02110307; Van Poucke S, 2016, PLOS ONE, V11, DOI 10.1371/journal.pone.0145791; Verberkmoes NJ, 2012, NETH HEART J, V20, P193, DOI 10.1007/s12471-012-0258-x; Wan-Hui W., 2009, COMP SCI INF ENG 200, V4; Wesolowski A, 2012, SCIENCE, V338, P267, DOI 10.1126/science.1223467; Younis E.M., 2015, INT J COMPUT APPL, V112	65	0	0	159	159	ELSEVIER SCIENCE BV	AMSTERDAM	PO BOX 211, 1000 AE AMSTERDAM, NETHERLANDS	1566-2535	1872-6305		INFORM FUSION	Inf. Fusion	MAR	2018	40						18	31		10.1016/j.inffus.2017.05.005				14	Computer Science, Artificial Intelligence; Computer Science, Theory & Methods	Computer Science	FJ9AG	WOS:000413059200002		gold			2018-02-07	"""

        line_to_parse = line_to_parse.strip(" ")
        line_to_parse = line_to_parse.strip("\r")
        parseable_lines = []
        lines_with_errors = []
        repaired_lines = parse_line(line_to_parse, 68, parseable_lines, lines_with_errors)
        self.assertEqual(True, len(parseable_lines) == 1 and repaired_lines == 1)

    """
    This test tests that an erroneous line (with some columns missing, some remaining) is rejected by the system.
    """
    def test_parse_line_for_invalid_line(self):
        erroneous_line = """J	Kanjo, E; Younis, EMG; Sherkat, N				Kanjo, Eiman; Younis, Eman M. G.; Sherkat, Nasser			Towards unravelling the relationship between on-body, environmental and emotion data using sensor information fusion approach	INFORMATION FUSION			English	Article						Multi sensor data fusion; Regression analysis sensor data; Multivariable regression; Affective computing; Physiological signals; Machine learning	AIR-POLLUTION; NOISE EXPOSURE; HUMAN MOBILITY; GLOBAL BURDEN; FRAMEWORK; NETWORK; DISEASE; QUALITY; SYSTEMS; MODELS	Over the past few years, there has been a noticeable advancement in environmental models and information fusion systems taking advantage of the recent developments in sensor and mobile technologies. However, little attention has been paid so far to quantifying the relationship between environment changes and their impact on our bodies in real-life settings. In this paper, we identify a data driven approach based on direct and continuous sensor data to assess the impact of the surrounding environment and physiological changes and emotion. We aim at investigating the potential of fusing on-body physiological signals, environmental sensory data and on-line self-report emotion measures in order to achieve the following objectives: (1) model the short term impact of the ambient environment on human body, (2) predict emotions based on-body sensors and environmental data. To achieve this, we have conducted a real-world study 'in the wild' with on-body and mobile sensors. Data was collected from participants walking around Nottingham city centre, in order to develop analytical and predictive models. Multiple regression, after allowing for possible confounders, showed a noticeable correlation between noise exposure and heart rate. Similarly, UV and environmental noise have been shown to have a noticeable effect on changes in ElectroDermal Activity (EDA). Air pressure demonstrated 10.1016/j.scitotenv.2010.03.018; Stansfeld S, 2000, Rev Environ Health, V15, P43; Steinle S, 2015, SCI TOTAL ENVIRON, V508, P383, DOI 10.1016/j.scitotenv.2014.12.003; Steinle S, 2013, SCI TOTAL ENVIRON, V443, P184, DOI 10.1016/j.scitotenv.2012.10.098; Takahashi K, 2004, RO-MAN 2004: 13TH IEEE INTERNATIONAL WORKSHOP ON ROBOT AND HUMAN INTERACTIVE COMMUNICATION, PROCEEDINGS, P95, DOI 10.1109/ROMAN.2004.1374736; Valstar M., 2016, ARXIV160501600; van Kempen EEMM, 2002, ENVIRON HEALTH PERSP, V110, P307, DOI 10.1289/ehp.02110307; Van Poucke S, 2016, PLOS ONE, V11, DOI 10.1371/journal.pone.0145791; Verberkmoes NJ, 2012, NETH HEART J, V20, P193, DOI 10.1007/s12471-012-0258-x; Wan-Hui W., 2009, COMP SCI INF ENG 200, V4; Wesolowski A, 2012, SCIENCE, V338, P267, DOI 10.1126/science.1223467; Younis E.M., 2015, INT J COMPUT APPL, V112	65	0	0	159	159	ELSEVIER SCIENCE BV	AMSTERDAM	PO BOX 211, 1000 AE AMSTERDAM, NETHERLANDS	1566-2535	1872-6305		INFORM FUSION	Inf. Fusion	MAR	2018	40						18	31		10.1016/j.inffus.2017.05.005				14	Computer Science, Artificial Intelligence; Computer Science, Theory & Methods	Computer Science	FJ9AG	WOS:000413059200002		gold			2018-02-07	"""

        erroneous_line = erroneous_line.strip(" ")
        erroneous_line = erroneous_line.strip("\r")
        parseable_lines = []
        lines_with_errors = []
        repaired_lines = parse_line(erroneous_line, 68, parseable_lines, lines_with_errors)
        self.assertEqual(True, len(lines_with_errors) == 1)

    """
    This test tests that a blank line is not processed by the system (i.e. does not appear in statistics,
    but instead is directly discarded by parse_line)
    """
    def test_parse_line_for_blank_line(self):
        erroneous_line = ""
        erroneous_line = erroneous_line.strip(" ")
        erroneous_line = erroneous_line.strip("\r")
        parseable_lines = []
        lines_with_errors = []
        repaired_lines = parse_line(erroneous_line, 68, parseable_lines, lines_with_errors)
        self.assertEqual(True, len(lines_with_errors) == 0 and len(parseable_lines) == 0)

    """
    This test tests that upon calling write_report on some data, this data will be correctly written to the
    designated files.
    """
    def test_write_report(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        parseable_lines = ["my_first_parseable_line", "my_second_parseable_line"]
        lines_with_errors = ["error 1", "error 2"]
        onefile_output = open(os.path.join(dir, "testFiles/dummy_onefilecorpus.txt"), "w")
        errorsfile_output = open(os.path.join(dir, "testFiles/dummy_errorsfile.txt"), "w")

        write_report(parseable_lines, lines_with_errors, onefile_output, errorsfile_output)
        onefile_output.close()
        errorsfile_output.close()

        onefile_output_read = open(os.path.join(dir, "testFiles/dummy_onefilecorpus.txt"), "r")
        errorsfile_output_read = open(os.path.join(dir, "testFiles/dummy_errorsfile.txt"), "r")

        onefile_output_lines = onefile_output_read.readlines()
        errorsfile_output_lines = errorsfile_output_read.readlines()

        result = True
        if len(onefile_output_lines) != 2 or len(errorsfile_output_lines) != 2:
            result = False

        if onefile_output_lines != ['my_first_parseable_line\n', 'my_second_parseable_line\n']:
            result = False

        onefile_output_read.close()
        errorsfile_output_read.close()
        os.remove(os.path.join(dir, "testFiles/dummy_onefilecorpus.txt"))
        os.remove(os.path.join(dir, "testFiles/dummy_errorsfile.txt"))
        self.assertEqual(True, result)

    """
    This test tests that upon calling prepare_output_file with some headers and an output file,
    the file is properly created and contains headers.
    """
    def test_prepare_output_file(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        headers_to_write = "abcd"
        prepare_output_file(os.path.join(dir, "testFiles/test_prepare_output_file.txt"), headers_to_write)

        result = open(os.path.join(dir, "testFiles/test_prepare_output_file.txt"), "r")
        lines = result.readlines()
        result.close()
        os.remove(os.path.join(dir, "testFiles/test_prepare_output_file.txt"))
        self.assertEqual(lines, ['abcd\n'])

    """
    This test tests that upon calling prepare_report_directory,
    a report directory is created at the given path.
    """
    def test_prepare_report_directory(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        prepare_report_directory(os.path.join(dir, "testFiles/test_prepare_report_directory"))
        self.assertEqual(True, os.path.exists(os.path.join(dir, "testFiles/test_prepare_report_directory")))
        if os.path.exists(os.path.join(dir, "testFiles/test_prepare_report_directory")):
            os.rmdir(os.path.join(dir, "testFiles/test_prepare_report_directory"))

    """
    This test tests that upon calling prepare_error_file, with a valid report directory, an error .csv
    file is created.
    """
    def test_prepare_error_file(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        prepare_report_directory(os.path.join(dir, "testFiles/test_prepare_report_directory"))
        prepare_error_file(os.path.join(dir, "testFiles/test_prepare_report_directory"), "abcd")
        self.assertEqual(True, os.path.exists(os.path.join(dir, "testFiles/test_prepare_report_directory/wos_lines_with_errors.csv")))
        os.remove(os.path.join(dir, "testFiles/test_prepare_report_directory/wos_lines_with_errors.csv"))
        os.rmdir(os.path.join(dir, "testFiles/test_prepare_report_directory"))

if __name__ == '__main__':
    unittest.main()