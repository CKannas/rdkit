# $Id$
#
#  Copyright (C) 2003-2008  Greg Landrum and Rational Discovery LLC
#         All Rights Reserved
#
""" This is a rough coverage test of the python wrapper

it's intended to be shallow, but broad

"""
from rdkit import RDConfig
import os,sys,tempfile
import unittest
from rdkit import DataStructs
from rdkit import Chem

def feq(v1,v2,tol2=1e-4):
  return abs(v1-v2)<=tol2

class TestCase(unittest.TestCase):
  def setUp(self):
    pass

  def test0Except(self):

    try:
      Chem.tossit()
    except IndexError:
      ok=1
    else:
      ok=0
    assert ok


  def test1Table(self):

    tbl = Chem.GetPeriodicTable()
    self.failUnless(tbl)

    self.failUnless(feq(tbl.GetAtomicWeight(6),12.011))
    self.failUnless(feq(tbl.GetAtomicWeight("C"),12.011))
    self.failUnless(tbl.GetAtomicNumber('C')==6)
    self.failUnless(feq(tbl.GetRvdw(6),1.950))
    self.failUnless(feq(tbl.GetRvdw("C"),1.950))
    self.failUnless(feq(tbl.GetRcovalent(6),0.680))
    self.failUnless(feq(tbl.GetRcovalent("C"),0.680))
    self.failUnless(tbl.GetDefaultValence(6)==4)
    self.failUnless(tbl.GetDefaultValence("C")==4)
    self.failUnless(tuple(tbl.GetValenceList(6))==(4,))
    self.failUnless(tuple(tbl.GetValenceList("C"))==(4,))
    self.failUnless(tuple(tbl.GetValenceList(16))==(2,4,6))
    self.failUnless(tuple(tbl.GetValenceList("S"))==(2,4,6))
    self.failUnless(tbl.GetNOuterElecs(6)==4)
    self.failUnless(tbl.GetNOuterElecs("C")==4)

  def test2Atom(self):
    atom = Chem.Atom(6)
    self.failUnless(atom)
    self.failUnless(atom.GetAtomicNum()==6)
    atom.SetAtomicNum(8)
    self.failUnless(atom.GetAtomicNum()==8)

    atom = Chem.Atom("C")
    self.failUnless(atom)
    self.failUnless(atom.GetAtomicNum()==6)


  def test3Bond(self):
    # No longer relevant, bonds are not constructible from Python
    pass

  def test4Mol(self):
    mol = Chem.Mol()
    self.failUnless(mol)

  def test5Smiles(self):
    mol = Chem.MolFromSmiles('n1ccccc1')
    self.failUnless(mol)
    self.failUnless(mol.GetNumAtoms()==6)
    self.failUnless(mol.GetNumAtoms(1)==6)
    self.failUnless(mol.GetNumAtoms(0)==11)
    at = mol.GetAtomWithIdx(2)
    self.failUnless(at.GetAtomicNum()==6)
    at = mol.GetAtomWithIdx(0)
    self.failUnless(at.GetAtomicNum()==7)
    
  def _test6Bookmarks(self):
    mol = Chem.MolFromSmiles('n1ccccc1')
    self.failUnless(mol)

    self.failUnless(not mol.HasAtomBookmark(0))
    mol.SetAtomBookmark(mol.GetAtomWithIdx(0),0)
    mol.SetAtomBookmark(mol.GetAtomWithIdx(1),1)
    self.failUnless(mol.HasAtomBookmark(0))
    self.failUnless(mol.HasAtomBookmark(1))

    if 1:
      self.failUnless(not mol.HasBondBookmark(0))
      self.failUnless(not mol.HasBondBookmark(1))
      mol.SetBondBookmark(mol.GetBondWithIdx(0),0)
      mol.SetBondBookmark(mol.GetBondWithIdx(1),1)
      self.failUnless(mol.HasBondBookmark(0))
      self.failUnless(mol.HasBondBookmark(1))


    at = mol.GetAtomWithBookmark(0)
    self.failUnless(at)
    self.failUnless(at.GetAtomicNum()==7)
    mol.ClearAtomBookmark(0)
    self.failUnless(not mol.HasAtomBookmark(0))
    self.failUnless(mol.HasAtomBookmark(1))
    mol.ClearAllAtomBookmarks()
    self.failUnless(not mol.HasAtomBookmark(0))
    self.failUnless(not mol.HasAtomBookmark(1))
    
    mol.SetAtomBookmark(mol.GetAtomWithIdx(1),1)

    if 1:
      self.failUnless(mol.HasBondBookmark(0))
      self.failUnless(mol.HasBondBookmark(1))
      bond = mol.GetBondWithBookmark(0)
      self.failUnless(bond)
      mol.ClearBondBookmark(0)
      self.failUnless(not mol.HasBondBookmark(0))
      self.failUnless(mol.HasBondBookmark(1))
      mol.ClearAllBondBookmarks()
      self.failUnless(not mol.HasBondBookmark(0))
      self.failUnless(not mol.HasBondBookmark(1))

      self.failUnless(mol.HasAtomBookmark(1))
    
  def test7Atom(self):
    mol = Chem.MolFromSmiles('n1ccccc1C[CH2-]')
    self.failUnless(mol)
    Chem.SanitizeMol(mol)
    a0 = mol.GetAtomWithIdx(0)
    a1 = mol.GetAtomWithIdx(1)
    a6 = mol.GetAtomWithIdx(6)
    a7 = mol.GetAtomWithIdx(7)
    
    self.failUnless(a0.GetAtomicNum()==7)
    self.failUnless(a0.GetSymbol()=='N')
    self.failUnless(a0.GetIdx()==0)

    aList = [a0,a1,a6,a7]
    self.failUnless(a0.GetDegree()==2)
    self.failUnless(a1.GetDegree()==2)
    self.failUnless(a6.GetDegree()==2)
    self.failUnless(a7.GetDegree()==1)
    self.failUnless([x.GetDegree() for x in aList]==[2,2,2,1])

    self.failUnless([x.GetTotalNumHs() for x in aList]==[0,1,2,2])
    self.failUnless([x.GetNumImplicitHs() for x in aList]==[0,1,2,0])
    self.failUnless([x.GetExplicitValence() for x in aList]==[3,3,2,3])
    self.failUnless([x.GetImplicitValence() for x in aList]==[0,1,2,0])
    self.failUnless([x.GetFormalCharge() for x in aList]==[0,0,0,-1])
    self.failUnless([x.GetNoImplicit() for x in aList]==[0,0,0,1])
    self.failUnless([x.GetNumExplicitHs() for x in aList]==[0,0,0,2])
    self.failUnless([x.GetIsAromatic() for x in aList]==[1,1,0,0])
    self.failUnless([x.GetHybridization() for x in aList]==[Chem.HybridizationType.SP2,Chem.HybridizationType.SP2,
                                                   Chem.HybridizationType.SP3,Chem.HybridizationType.SP3],\
                                                   [x.GetHybridization() for x in aList])
    


  def test8Bond(self):
    mol = Chem.MolFromSmiles('n1ccccc1CC(=O)O')
    self.failUnless(mol)
    Chem.SanitizeMol(mol)
    # note bond numbering is funny because of ring closure
    b0 = mol.GetBondWithIdx(0)
    b6 = mol.GetBondWithIdx(6)
    b7 = mol.GetBondWithIdx(7)
    b8 = mol.GetBondWithIdx(8)

    bList = [b0,b6,b7,b8]
    self.failUnless([x.GetBondType() for x in bList] ==
           [Chem.BondType.AROMATIC,Chem.BondType.SINGLE,
            Chem.BondType.DOUBLE,Chem.BondType.SINGLE])
    self.failUnless([x.GetIsAromatic() for x in bList] == 
           [1,0,0,0])
    
    self.failUnless([x.GetIsConjugated()!=0 for x in bList] ==
           [1,0,1,1],[x.GetIsConjugated()!=0 for x in bList])
    self.failUnless([x.GetBeginAtomIdx() for x in bList] ==
           [0,6,7,7],[x.GetBeginAtomIdx() for x in bList])
    self.failUnless([x.GetBeginAtom().GetIdx() for x in bList] ==
           [0,6,7,7])
    self.failUnless([x.GetEndAtomIdx() for x in bList] ==
           [1,7,8,9])
    self.failUnless([x.GetEndAtom().GetIdx() for x in bList] ==
           [1,7,8,9])


  def test9Smarts(self):
    query1 = Chem.MolFromSmarts('C(=O)O')
    self.failUnless(query1)
    query2 = Chem.MolFromSmarts('C(=O)[O,N]')
    self.failUnless(query2)
    query3 = Chem.MolFromSmarts('[$(C(=O)O)]')
    self.failUnless(query3)


    mol = Chem.MolFromSmiles('CCC(=O)O')
    self.failUnless(mol)

    self.failUnless(mol.HasSubstructMatch(query1))
    self.failUnless(mol.HasSubstructMatch(query2))
    self.failUnless(mol.HasSubstructMatch(query3))

    mol = Chem.MolFromSmiles('CCC(=O)N')
    self.failUnless(mol)

    self.failUnless(not mol.HasSubstructMatch(query1))
    self.failUnless(mol.HasSubstructMatch(query2))
    self.failUnless(not mol.HasSubstructMatch(query3))

  def test10Iterators(self):
    mol = Chem.MolFromSmiles('CCOC')
    self.failUnless(mol)

    for atom in mol.GetAtoms():
      self.failUnless(atom)
    ats = mol.GetAtoms()
    try:
      ats[1]
    except:
      ok = 0
    else:
      ok = 1
    self.failUnless(ok)
    try:
      ats[12]
    except IndexError:
      ok = 1
    else:
      ok = 0
    self.failUnless(ok)

    if 0:
      for atom in mol.GetHeteros():
        self.failUnless(atom)
      ats = mol.GetHeteros()
      try:
        ats[0]
      except:
        ok = 0
      else:
        ok = 1
      self.failUnless(ok)
      self.failUnless(ats[0].GetIdx()==2)
      try:
        ats[12]
      except IndexError:
        ok = 1
      else:
        ok = 0
      self.failUnless(ok)


    for bond in mol.GetBonds():
      self.failUnless(bond)
    bonds = mol.GetBonds()
    try:
      bonds[1]
    except:
      ok = 0
    else:
      ok = 1
    self.failUnless(ok)
    try:
      bonds[12]
    except IndexError:
      ok = 1
    else:
      ok = 0
    self.failUnless(ok)
      
    if 0:
      mol = Chem.MolFromSmiles('c1ccccc1C')
      for atom in mol.GetAromaticAtoms():
        self.failUnless(atom)
      ats = mol.GetAromaticAtoms()
      try:
        ats[0]
      except:
        ok = 0
      else:
        ok = 1
      self.failUnless(ok)
      self.failUnless(ats[0].GetIdx()==0)
      self.failUnless(ats[1].GetIdx()==1)
      self.failUnless(ats[2].GetIdx()==2)
      try:
        ats[12]
      except IndexError:
        ok = 1
      else:
        ok = 0
      self.failUnless(ok)




  def test11MolOps(self) :
    mol = Chem.MolFromSmiles('C1=CC=C(C=C1)P(C2=CC=CC=C2)C3=CC=CC=C3')
    self.failUnless(mol)
    smi = Chem.MolToSmiles(mol)
    Chem.SanitizeMol(mol)
    nr = Chem.GetSymmSSSR(mol)

    self.failUnless((len(nr) == 3))
    
  def test12Smarts(self):
    query1 = Chem.MolFromSmarts('C(=O)O')
    self.failUnless(query1)
    query2 = Chem.MolFromSmarts('C(=O)[O,N]')
    self.failUnless(query2)
    query3 = Chem.MolFromSmarts('[$(C(=O)O)]')
    self.failUnless(query3)


    mol = Chem.MolFromSmiles('CCC(=O)O')
    self.failUnless(mol)

    self.failUnless(mol.HasSubstructMatch(query1))
    self.failUnless(mol.GetSubstructMatch(query1)==(2,3,4))
    self.failUnless(mol.HasSubstructMatch(query2))
    self.failUnless(mol.GetSubstructMatch(query2)==(2,3,4))
    self.failUnless(mol.HasSubstructMatch(query3))
    self.failUnless(mol.GetSubstructMatch(query3)==(2,))

    mol = Chem.MolFromSmiles('CCC(=O)N')
    self.failUnless(mol)

    self.failUnless(not mol.HasSubstructMatch(query1))
    self.failUnless(not mol.GetSubstructMatch(query1))
    self.failUnless(mol.HasSubstructMatch(query2))
    self.failUnless(mol.GetSubstructMatch(query2)==(2,3,4))
    self.failUnless(not mol.HasSubstructMatch(query3))

    mol = Chem.MolFromSmiles('OC(=O)CC(=O)O')
    self.failUnless(mol)
    self.failUnless(mol.HasSubstructMatch(query1))
    self.failUnless(mol.GetSubstructMatch(query1)==(1,2,0))
    self.failUnless(mol.GetSubstructMatches(query1)==((1,2,0),(4,5,6)))
    self.failUnless(mol.HasSubstructMatch(query2))
    self.failUnless(mol.GetSubstructMatch(query2)==(1,2,0))
    self.failUnless(mol.GetSubstructMatches(query2)==((1,2,0),(4,5,6)))
    self.failUnless(mol.HasSubstructMatch(query3))
    self.failUnless(mol.GetSubstructMatches(query3)==((1,),(4,)))
    
  def test13Smarts(self):
    # previous smarts problems:
    query = Chem.MolFromSmarts('N(=,-C)')
    self.failUnless(query)
    mol = Chem.MolFromSmiles('N#C')
    self.failUnless(not mol.HasSubstructMatch(query))
    mol = Chem.MolFromSmiles('N=C')
    self.failUnless(mol.HasSubstructMatch(query))
    mol = Chem.MolFromSmiles('NC')
    self.failUnless(mol.HasSubstructMatch(query))

    query = Chem.MolFromSmarts('[Cl,$(O)]')
    mol = Chem.MolFromSmiles('C(=O)O')
    self.failUnless(len(mol.GetSubstructMatches(query))==2)
    mol = Chem.MolFromSmiles('C(=N)N')
    self.failUnless(len(mol.GetSubstructMatches(query))==0)
    
    query = Chem.MolFromSmarts('[$([O,S]-[!$(*=O)])]')
    mol = Chem.MolFromSmiles('CC(S)C(=O)O')
    self.failUnless(len(mol.GetSubstructMatches(query))==1)
    mol = Chem.MolFromSmiles('C(=O)O')
    self.failUnless(len(mol.GetSubstructMatches(query))==0)
    
    
  def test14Hs(self):
    m = Chem.MolFromSmiles('CC(=O)[OH]')
    self.failUnless(m.GetNumAtoms()==4)

    m2 = Chem.AddHs(m,1)
    self.failUnless(m2.GetNumAtoms()==5)
    m2 = Chem.RemoveHs(m2,1)
    self.failUnless(m2.GetNumAtoms()==5)
    m2 = Chem.RemoveHs(m2,0)
    self.failUnless(m2.GetNumAtoms()==4)
    
    m2 = Chem.AddHs(m,0)
    self.failUnless(m2.GetNumAtoms()==8)
    m2 = Chem.RemoveHs(m2,1)
    self.failUnless(m2.GetNumAtoms()==5)
    m2 = Chem.RemoveHs(m2)
    self.failUnless(m2.GetNumAtoms()==4)

    m = Chem.MolFromSmiles('CC[H]',False)
    self.failUnless(m.GetNumAtoms()==3)
    m2 = Chem.MergeQueryHs(m)
    self.failUnless(m2.GetNumAtoms()==2)
    self.failUnless(m2.GetAtomWithIdx(1).HasQuery())
    
  def test15Neighbors(self):
    m = Chem.MolFromSmiles('CC(=O)[OH]')
    self.failUnless(m.GetNumAtoms()==4)
    
    a = m.GetAtomWithIdx(1)
    ns = a.GetNeighbors()
    self.failUnless(len(ns)==3)

    bs = a.GetBonds()
    self.failUnless(len(bs)==3)

    for b in bs:
      try:
        a2 = b.GetOtherAtom(a)
      except:
        a2=None
      self.failUnless(a2)
    self.failUnless(len(bs)==3)

  def test16Pickle(self):
    import cPickle
    m = Chem.MolFromSmiles('C1=CN=CC=C1')
    pkl = cPickle.dumps(m)
    m2 = cPickle.loads(pkl)
    smi1 = Chem.MolToSmiles(m)
    smi2 = Chem.MolToSmiles(m2)
    self.failUnless(smi1==smi2)
    
  def test16Props(self):
    m = Chem.MolFromSmiles('C1=CN=CC=C1')
    self.failUnless(not m.HasProp('prop1'))
    self.failUnless(not m.HasProp('prop2'))
    self.failUnless(not m.HasProp('prop2'))
    m.SetProp('prop1','foob')
    self.failUnless(not m.HasProp('prop2'))
    self.failUnless(m.HasProp('prop1'))
    self.failUnless(m.GetProp('prop1')=='foob')
    self.failUnless(not m.HasProp('propo'))
    try:
      m.GetProp('prop2')
    except KeyError:
      ok=1
    else:
      ok=0
    self.failUnless(ok)

    # test computed properties
    m.SetProp('cprop1', 'foo', 1)
    m.SetProp('cprop2', 'foo2', 1)

    m.ClearComputedProps()
    self.failUnless(not m.HasProp('cprop1'))
    self.failUnless(not m.HasProp('cprop2'))

  def test17Kekulize(self):
    m = Chem.MolFromSmiles('c1ccccc1')
    smi = Chem.MolToSmiles(m)
    self.failUnless(smi=='c1ccccc1')

    Chem.Kekulize(m)
    smi = Chem.MolToSmiles(m)
    self.failUnless(smi=='c1ccccc1')

    m = Chem.MolFromSmiles('c1ccccc1')
    smi = Chem.MolToSmiles(m)
    self.failUnless(smi=='c1ccccc1')

    Chem.Kekulize(m,1)
    smi = Chem.MolToSmiles(m)
    self.failUnless(smi=='C1=CC=CC=C1', smi)
    
  def test20IsInRing(self):
    m = Chem.MolFromSmiles('C1CCC1C')
    self.failUnless(m)
    self.failUnless(m.GetAtomWithIdx(0).IsInRingSize(4))
    self.failUnless(m.GetAtomWithIdx(1).IsInRingSize(4))
    self.failUnless(m.GetAtomWithIdx(2).IsInRingSize(4))
    self.failUnless(m.GetAtomWithIdx(3).IsInRingSize(4))
    self.failUnless(not m.GetAtomWithIdx(4).IsInRingSize(4))
    
    self.failUnless(not m.GetAtomWithIdx(0).IsInRingSize(3))
    self.failUnless(not m.GetAtomWithIdx(1).IsInRingSize(3))
    self.failUnless(not m.GetAtomWithIdx(2).IsInRingSize(3))
    self.failUnless(not m.GetAtomWithIdx(3).IsInRingSize(3))
    self.failUnless(not m.GetAtomWithIdx(4).IsInRingSize(3))
    
    self.failUnless(m.GetBondWithIdx(0).IsInRingSize(4))
    self.failUnless(not m.GetBondWithIdx(3).IsInRingSize(4))
    self.failUnless(not m.GetBondWithIdx(0).IsInRingSize(3))
    self.failUnless(not m.GetBondWithIdx(3).IsInRingSize(3))
    
  def test21Robustification(self):
    ok = False
    # FIX: at the moment I can't figure out how to catch the
    # actual exception that BPL is throwinng when it gets
    # invalid arguments (Boost.Python.ArgumentError)
    try:
      Chem.MolFromSmiles('C=O').HasSubstructMatch(Chem.MolFromSmarts('fiib'))
    #except ValueError:
    #  ok=True
    except:
      ok=True
    self.failUnless(ok  )

  def test23MolFileParsing(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','triazine.mol')
    #fileN = "../FileParsers/test_data/triazine.mol"
    inD = open(fileN,'r').read()
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==9)

    m1 = Chem.MolFromMolFile(fileN)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==9)

    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','triazine.mof')
    self.failUnlessRaises(IOError,lambda :Chem.MolFromMolFile(fileN))

    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','list-query.mol')
    query = Chem.MolFromMolFile(fileN)
    smi = Chem.MolToSmiles(query)
    self.failUnless(smi=='c1ccccc1')
    smi = Chem.MolToSmarts(query)
    self.failUnless(smi=='[#6]1:[#6]:[#6]:[#6]:[#6]:[#6,#7,#15]:1',smi)

    query = Chem.MolFromMolFile(fileN,sanitize=False)
    smi = Chem.MolToSmiles(query)
    self.failUnless(smi=='C1=CC=CC=C1')
    smi = Chem.MolToSmarts(query)
    self.failUnless(smi=='[#6]1=[#6]-[#6]=[#6]-[#6]=[#6,#7,#15]-1')
    smi = "C1=CC=CC=C1"
    mol = Chem.MolFromSmiles(smi,0)
    self.failUnless(mol.HasSubstructMatch(query))
    Chem.SanitizeMol(mol)
    self.failUnless(not mol.HasSubstructMatch(query))

    mol = Chem.MolFromSmiles('N1=CC=CC=C1',0)
    self.failUnless(mol.HasSubstructMatch(query))
    mol = Chem.MolFromSmiles('S1=CC=CC=C1',0)
    self.failUnless(not mol.HasSubstructMatch(query))
    mol = Chem.MolFromSmiles('P1=CC=CC=C1',0)
    self.failUnless(mol.HasSubstructMatch(query))


    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','issue123.mol')
    mol = Chem.MolFromMolFile(fileN)
    self.failUnless(mol)
    self.failUnless(mol.GetNumAtoms()==23)
    mol = Chem.MolFromMolFile(fileN,removeHs=False)
    self.failUnless(mol)
    self.failUnless(mol.GetNumAtoms()==39)

  def test25SDMolSupplier(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','NCI_aids_few.sdf')
    #fileN = "../FileParsers/test_data/NCI_aids_few.sdf"
    sdSup = Chem.SDMolSupplier(fileN)
    molNames = ["48", "78", "128", "163", "164", "170", "180", "186",
            "192", "203", "210", "211", "213", "220", "229", "256"]

    chgs192 = {8:1, 11:1, 15:-1, 18:-1, 20:1, 21:1, 23:-1, 25:-1} 
    i = 0
    for mol in sdSup :
      self.failUnless(mol)
      self.failUnless(mol.GetProp("_Name") == molNames[i])
      i += 1
      if (mol.GetProp("_Name") == "192") :
        # test parsed charges on one of the molecules
        for id in chgs192.keys() :
          self.failUnless(mol.GetAtomWithIdx(id).GetFormalCharge() == chgs192[id])
          
    sdSup.reset()
    
    ns = [mol.GetProp("_Name") for mol in sdSup]
    self.failUnless(ns == molNames)

    sdSup = Chem.SDMolSupplier(fileN, 0)
    for mol in sdSup :
      self.failUnless(not mol.HasProp("numArom"))

    sdSup = Chem.SDMolSupplier(fileN)
    self.failUnless(len(sdSup) == 16)
    mol = sdSup[5]
    self.failUnless(mol.GetProp("_Name") == "170")


    # test handling of H removal:
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','withHs.sdf')
    sdSup = Chem.SDMolSupplier(fileN)
    m = sdSup.next()
    self.failUnless(m)
    self.failUnless(m.GetNumAtoms()==23)
    m = sdSup.next()
    self.failUnless(m)
    print m.GetNumAtoms()
    self.failUnless(m.GetNumAtoms()==28)

    sdSup = Chem.SDMolSupplier(fileN,removeHs=False)
    m = sdSup.next()
    self.failUnless(m)
    self.failUnless(m.GetNumAtoms()==39)
    m = sdSup.next()
    self.failUnless(m)
    self.failUnless(m.GetNumAtoms()==30)

    d = file(fileN,'r').read()
    sdSup.SetData(d)
    m = sdSup.next()
    self.failUnless(m)
    self.failUnless(m.GetNumAtoms()==23)
    m = sdSup.next()
    self.failUnless(m)
    print m.GetNumAtoms()
    self.failUnless(m.GetNumAtoms()==28)

    sdSup.SetData(d,removeHs=False)
    m = sdSup.next()
    self.failUnless(m)
    self.failUnless(m.GetNumAtoms()==39)
    m = sdSup.next()
    self.failUnless(m)
    self.failUnless(m.GetNumAtoms()==30)

    
  def test26SmiMolSupplier(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','first_200.tpsa.csv')
    #fileN = "../FileParsers/test_data/first_200.tpsa.csv"
    smiSup = Chem.SmilesMolSupplier(fileN, ",", 0, -1)
    mol = smiSup[16];
    self.failUnless(mol.GetProp("TPSA") == "46.25")

    mol = smiSup[8];
    self.failUnless(mol.GetProp("TPSA") == "65.18")

    self.failUnless(len(smiSup) == 200)

    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','fewSmi.csv')
    #fileN = "../FileParsers/test_data/fewSmi.csv"
    smiSup = Chem.SmilesMolSupplier(fileN, delimiter=",",
                                      smilesColumn=1, nameColumn=0,
                                      titleLine=0)
    names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    i = 0
    for mol in smiSup:
      self.failUnless(mol.GetProp("_Name") == names[i])
      i += 1
      
    mol = smiSup[3]
    
    self.failUnless(mol.GetProp("_Name") == "4")
    self.failUnless(mol.GetProp("Column_2") == "82.78")

    # and test doing a supplier from text:
    inD = open(fileN,'r').read()
    smiSup.SetData(inD, delimiter=",",
                   smilesColumn=1, nameColumn=0,
                   titleLine=0)
    names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    i = 0
    # iteration interface:
    for mol in smiSup:
      self.failUnless(mol.GetProp("_Name") == names[i])
      i += 1
    self.failUnless(i==10)
    # random access:
    mol = smiSup[3]
    self.failUnless(len(smiSup)==10)
    self.failUnless(mol.GetProp("_Name") == "4")
    self.failUnless(mol.GetProp("Column_2") == "82.78")

    # issue 113:
    smiSup.SetData(inD, delimiter=",",
                   smilesColumn=1, nameColumn=0,
                   titleLine=0)
    self.failUnless(len(smiSup)==10)

    # and test failure handling:
    inD = """mol-1,CCC
mol-2,CCCC
mol-3,fail
mol-4,CCOC
    """
    smiSup.SetData(inD, delimiter=",",
                   smilesColumn=1, nameColumn=0,
                   titleLine=0)
    # there are 4 entries in the supplier:
    self.failUnless(len(smiSup)==4)
    # but the 3rd is a None:
    self.failUnless(smiSup[2] is None)


    text="Id SMILES Column_2\n"+\
    "mol-1 C 1.0\n"+\
    "mol-2 CC 4.0\n"+\
    "mol-4 CCCC 16.0"
    smiSup.SetData(text, delimiter=" ",
                   smilesColumn=1, nameColumn=0,
                   titleLine=1)
    self.failUnless(len(smiSup)==3)
    self.failUnless(smiSup[0])
    self.failUnless(smiSup[1])
    self.failUnless(smiSup[2])
    m = [x for x in smiSup]
    self.failUnless(smiSup[2])
    self.failUnless(len(m)==3)
    self.failUnless(m[0].GetProp("Column_2")=="1.0")
    
    # test simple parsing and Issue 114:
    smis = ['CC','CCC','CCOC','CCCOCC','CCCOCCC']
    inD = '\n'.join(smis)
    smiSup.SetData(inD, delimiter=",",
                   smilesColumn=0, nameColumn=-1,
                   titleLine=0)
    self.failUnless(len(smiSup)==5)
    m = [x for x in smiSup]
    self.failUnless(smiSup[4])
    self.failUnless(len(m)==5)
    
    # order dependance:
    smiSup.SetData(inD, delimiter=",",
                   smilesColumn=0, nameColumn=-1,
                   titleLine=0)
    self.failUnless(smiSup[4])
    self.failUnless(len(smiSup)==5)

    # this was a nasty BC:
    # asking for a particular entry with a higher index than what we've
    # already seen resulted in a duplicate:
    smis = ['CC','CCC','CCOC','CCCCOC']
    inD = '\n'.join(smis)
    smiSup.SetData(inD, delimiter=",",
                   smilesColumn=0, nameColumn=-1,
                   titleLine=0)
    m = smiSup.next()
    m = smiSup[3]
    self.failUnless(len(smiSup)==4)

    try:
      smiSup[4]
    except:
      ok=1
    else:
      ok=0
    self.failUnless(ok)

    smiSup.SetData(inD, delimiter=",",
                   smilesColumn=0, nameColumn=-1,
                   titleLine=0)
    try:
      smiSup[4]
    except:
      ok=1
    else:
      ok=0
    self.failUnless(ok)
    sys.stderr.write('>>> This may result in an infinite loop.  It should finish almost instantly\n')
    self.failUnless(len(smiSup)==4)
    sys.stderr.write('<<< OK, it finished.\n')


  def test27SmilesWriter(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','fewSmi.csv')
    #fileN = "../FileParsers/test_data/fewSmi.csv"

    smiSup = Chem.SmilesMolSupplier(fileN, delimiter=",",
                                      smilesColumn=1, nameColumn=0,
                                      titleLine=0)
    propNames = []
    propNames.append("Column_2")
    ofile = os.path.join(RDConfig.RDBaseDir,"Code","GraphMol","Wrap","test_data/outSmiles.txt")
    writer = Chem.SmilesWriter(ofile)
    writer.SetProps(propNames)
    for mol in smiSup :
      writer.write(mol)
    writer.flush()

  def test28SmilesReverse(self):
    names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    props = ["34.14","25.78","106.51","82.78","60.16","87.74","37.38","77.28","65.18","0.00"]
    ofile = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','Wrap','test_data','outSmiles.txt')
    #ofile = "test_data/outSmiles.csv"
    smiSup = Chem.SmilesMolSupplier(ofile)
    i = 0
    for mol in smiSup:
      #print [repr(x) for x in mol.GetPropNames()]
      self.failUnless(mol.GetProp("_Name") == names[i])
      self.failUnless(mol.GetProp("Column_2") == props[i])
      i += 1
      
  def writerSDFile(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','NCI_aids_few.sdf')
    #fileN = "../FileParsers/test_data/NCI_aids_few.sdf"
    ofile = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','Wrap','test_data','outNCI_few.sdf');
    writer = Chem.SDWriter(ofile);
    sdSup = Chem.SDMolSupplier(fileN)
    for mol in sdSup :
      writer.write(mol)
    writer.flush()

  def test29SDWriterLoop(self) :
    self.writerSDFile()
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','Wrap',
                                            'test_data','outNCI_few.sdf')
    sdSup = Chem.SDMolSupplier(fileN)
    molNames = ["48", "78", "128", "163", "164", "170", "180", "186",
            "192", "203", "210", "211", "213", "220", "229", "256"]
    chgs192 = {8:1, 11:1, 15:-1, 18:-1, 20:1, 21:1, 23:-1, 25:-1}
    i = 0
    
    for mol in sdSup :
      #print 'mol:',mol
      #print '\t',molNames[i]
      self.failUnless(mol.GetProp("_Name") == molNames[i])
      i += 1
      if (mol.GetProp("_Name") == "192") :
        # test parsed charges on one of the molecules
        for id in chgs192.keys() :
          self.failUnless(mol.GetAtomWithIdx(id).GetFormalCharge() == chgs192[id])

  def test30Issues109and110(self) :
    """ issues 110 and 109 were both related to handling of explicit Hs in
       SMILES input.
       
    """ 
    m1 = Chem.MolFromSmiles('N12[CH](SC(C)(C)[CH]1C(O)=O)[CH](C2=O)NC(=O)[CH](N)c3ccccc3')
    self.failUnless(m1.GetNumAtoms()==24)
    m2 = Chem.MolFromSmiles('C1C=C([CH](N)C(=O)N[C]2([H])[C]3([H])SC(C)(C)[CH](C(=O)O)N3C(=O)2)C=CC=1')
    self.failUnless(m2.GetNumAtoms()==24)

    smi1 = Chem.MolToSmiles(m1)
    smi2 = Chem.MolToSmiles(m2)
    self.failUnless(smi1==smi2)

    m1 = Chem.MolFromSmiles('[H]CCl')
    self.failUnless(m1.GetNumAtoms()==2)
    self.failUnless(m1.GetAtomWithIdx(0).GetNumExplicitHs()==0)
    m1 = Chem.MolFromSmiles('[H][CH2]Cl')
    self.failUnless(m1.GetNumAtoms()==2)
    self.failUnless(m1.GetAtomWithIdx(0).GetNumExplicitHs()==3)
    m2 = Chem.AddHs(m1)
    self.failUnless(m2.GetNumAtoms()==5)
    m2 = Chem.RemoveHs(m2)
    self.failUnless(m2.GetNumAtoms()==2)
    
  def test31ChiralitySmiles(self) :
    m1 = Chem.MolFromSmiles('F[C@](Br)(I)Cl')
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==5)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[C@](Cl)(Br)I',Chem.MolToSmiles(m1,1))

    m1 = Chem.MolFromSmiles('CC1C[C@@]1(Cl)F')
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==6)
    self.failUnless(Chem.MolToSmiles(m1,1)=='CC1C[C@]1(F)Cl',Chem.MolToSmiles(m1,1))

    m1 = Chem.MolFromSmiles('CC1C[C@]1(Cl)F')
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==6)
    self.failUnless(Chem.MolToSmiles(m1,1)=='CC1C[C@@]1(F)Cl',Chem.MolToSmiles(m1,1))


  def test31aChiralitySubstructs(self) :
    m1 = Chem.MolFromSmiles('CC1C[C@@]1(Cl)F')
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==6)
    self.failUnless(Chem.MolToSmiles(m1,1)=='CC1C[C@]1(F)Cl',Chem.MolToSmiles(m1,1))

    m2 = Chem.MolFromSmiles('CC1C[C@]1(Cl)F')
    self.failUnless(m2 is not None)
    self.failUnless(m2.GetNumAtoms()==6)
    self.failUnless(Chem.MolToSmiles(m2,1)=='CC1C[C@@]1(F)Cl',Chem.MolToSmiles(m2,1))

    self.failUnless(m1.HasSubstructMatch(m1))
    self.failUnless(m1.HasSubstructMatch(m2))
    self.failUnless(m1.HasSubstructMatch(m1,useChirality=True))
    self.failUnless(not m1.HasSubstructMatch(m2,useChirality=True))

    
    

  def _test32MolFilesWithChirality(self) :
    inD = """chiral1.mol
  ChemDraw10160313232D

  5  4  0  0  0  0  0  0  0  0999 V2000
    0.0553    0.6188    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.0553   -0.2062    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7697   -0.6188    0.0000 I   0  0  0  0  0  0  0  0  0  0  0  0
   -0.6592   -0.6188    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
   -0.7697   -0.2062    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  0      
  2  4  1  1      
  2  5  1  0      
M  END
"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==5)
    self.failUnless(smi=='F[C@](Cl)(Br)I',smi)

    inD = """chiral2.cdxml
  ChemDraw10160314052D

  5  4  0  0  0  0  0  0  0  0999 V2000
    0.0553    0.6188    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.0553   -0.2062    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.7697   -0.6188    0.0000 I   0  0  0  0  0  0  0  0  0  0  0  0
   -0.6592   -0.6188    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
   -0.7697   -0.2062    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  0      
  2  4  1  6      
  2  5  1  0      
M  END
"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==5)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[C@@](Cl)(Br)I')

    inD = """chiral1.mol
  ChemDraw10160313232D

  5  4  0  0  0  0  0  0  0  0999 V2000
    0.0553    0.6188    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.0553   -0.2062    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.7697   -0.2062    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
   -0.6592   -0.6188    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
    0.7697   -0.6188    0.0000 I   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  0      
  2  4  1  1      
  2  5  1  0      
M  END
"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==5)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[C@](Cl)(Br)I')

    inD = """chiral1.mol
  ChemDraw10160313232D

  5  4  0  0  0  0  0  0  0  0999 V2000
    0.0553   -0.2062    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.7697   -0.2062    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
   -0.6592   -0.6188    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
    0.7697   -0.6188    0.0000 I   0  0  0  0  0  0  0  0  0  0  0  0
    0.0553    0.6188    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  1  3  1  1      
  1  4  1  0     
  1  5  1  0      
M  END
"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==5)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[C@](Cl)(Br)I')

    inD = """chiral3.mol
  ChemDraw10160314362D

  4  3  0  0  0  0  0  0  0  0999 V2000
    0.4125    0.6188    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.4125   -0.2062    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.3020   -0.6188    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
   -0.4125   -0.2062    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  1      
  2  4  1  0      
M  END

"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==4)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[C@H](Cl)Br')

    inD = """chiral4.mol
  ChemDraw10160314362D

  4  3  0  0  0  0  0  0  0  0999 V2000
    0.4125    0.6188    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.4125   -0.2062    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
   -0.3020   -0.6188    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
   -0.4125   -0.2062    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  1      
  2  4  1  0      
M  END

"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==4)
    self.failUnless(Chem.MolToSmiles(m1,1)=='FN(Cl)Br')

    inD = """chiral5.mol
  ChemDraw10160314362D

  4  3  0  0  0  0  0  0  0  0999 V2000
    0.4125    0.6188    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.4125   -0.2062    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0
   -0.3020   -0.6188    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
   -0.4125   -0.2062    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  1      
  2  4  1  0      
M  CHG  1   2   1
M  END

"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==4)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[N@H+](Cl)Br')

    inD="""Case 10-14-3
  ChemDraw10140308512D

  4  3  0  0  0  0  0  0  0  0999 V2000
   -0.8250   -0.4125    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.8250   -0.4125    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    0.4125    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  0      
  2  4  1  1      
M  END
"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==4)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[C@H](Cl)Br')

    inD="""Case 10-14-4
  ChemDraw10140308512D

  4  3  0  0  0  0  0  0  0  0999 V2000
   -0.8250   -0.4125    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -0.4125    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.8250   -0.4125    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    0.4125    0.0000 Br  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  1      
  2  4  1  0      
M  END

"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==4)
    self.failUnless(Chem.MolToSmiles(m1,1)=='F[C@H](Cl)Br')

    inD="""chiral4.mol
  ChemDraw10160315172D

  6  6  0  0  0  0  0  0  0  0999 V2000
   -0.4422    0.1402    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.4422   -0.6848    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2723   -0.2723    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.8547    0.8547    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.6848    0.4422    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.8547   -0.8547    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  0      
  3  1  1  0      
  1  4  1  0      
  3  5  1  1      
  3  6  1  0      
M  END
"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==6)
    self.failUnless(Chem.MolToSmiles(m1,1)=='CC1C[C@@]1(F)Cl',Chem.MolToSmiles(m1,1))

    inD="""chiral4.mol
  ChemDraw10160315172D

  6  6  0  0  0  0  0  0  0  0999 V2000
   -0.4422    0.1402    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.4422   -0.6848    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.2723   -0.2723    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -0.8547    0.8547    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.6848    0.4422    0.0000 F   0  0  0  0  0  0  0  0  0  0  0  0
    0.8547   -0.8547    0.0000 Cl  0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0      
  2  3  1  0      
  3  1  1  0      
  1  4  1  0      
  3  5  1  6      
  3  6  1  0      
M  END
"""
    m1 = Chem.MolFromMolBlock(inD)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==6)
    self.failUnless(Chem.MolToSmiles(m1,1)=='CC1C[C@]1(F)Cl',Chem.MolToSmiles(m1,1))

  def test33Issue65(self) :
    """ issue 65 relates to handling of [H] in SMARTS
       
    """ 
    m1 = Chem.MolFromSmiles('OC(O)(O)O')
    m2 = Chem.MolFromSmiles('OC(O)O')
    m3 = Chem.MolFromSmiles('OCO')
    q1 = Chem.MolFromSmarts('OC[H]',1)
    q2 = Chem.MolFromSmarts('O[C;H1]',1)
    q3 = Chem.MolFromSmarts('O[C;H1][H]',1)

    self.failUnless(not m1.HasSubstructMatch(q1))
    self.failUnless(not m1.HasSubstructMatch(q2))
    self.failUnless(not m1.HasSubstructMatch(q3))

    self.failUnless(m2.HasSubstructMatch(q1))
    self.failUnless(m2.HasSubstructMatch(q2))
    self.failUnless(m2.HasSubstructMatch(q3))

    self.failUnless(m3.HasSubstructMatch(q1))
    self.failUnless(not m3.HasSubstructMatch(q2))
    self.failUnless(not m3.HasSubstructMatch(q3))

    m1H = Chem.AddHs(m1)
    m2H = Chem.AddHs(m2)
    m3H = Chem.AddHs(m3)
    q1 = Chem.MolFromSmarts('OC[H]')
    q2 = Chem.MolFromSmarts('O[C;H1]')
    q3 = Chem.MolFromSmarts('O[C;H1][H]')

    self.failUnless(not m1H.HasSubstructMatch(q1))
    self.failUnless(not m1H.HasSubstructMatch(q2))
    self.failUnless(not m1H.HasSubstructMatch(q3))

    #m2H.Debug()
    self.failUnless(m2H.HasSubstructMatch(q1))
    self.failUnless(m2H.HasSubstructMatch(q2))
    self.failUnless(m2H.HasSubstructMatch(q3))

    self.failUnless(m3H.HasSubstructMatch(q1))
    self.failUnless(not m3H.HasSubstructMatch(q2))
    self.failUnless(not m3H.HasSubstructMatch(q3))

  def test34Issue124(self) :
    """ issue 124 relates to calculation of the distance matrix
       
    """ 
    m = Chem.MolFromSmiles('CC=C')
    d = Chem.GetDistanceMatrix(m,0)
    self.failUnless(feq(d[0,1],1.0))
    self.failUnless(feq(d[0,2],2.0))
    # force an update:
    d = Chem.GetDistanceMatrix(m,1,0,1)
    self.failUnless(feq(d[0,1],1.0))
    self.failUnless(feq(d[0,2],1.5))

  def test35ChiralityPerception(self) :
    """ Test perception of chirality and CIP encoding       
    """ 
    m = Chem.MolFromSmiles('F[C@]([C@])(Cl)Br')
    Chem.AssignStereochemistry(m,1)
    self.failUnless(m.GetAtomWithIdx(1).HasProp('_CIPCode'))
    self.failIf(m.GetAtomWithIdx(2).HasProp('_CIPCode'))
    Chem.RemoveStereochemistry(m)
    self.failIf(m.GetAtomWithIdx(1).HasProp('_CIPCode'))

    
    m = Chem.MolFromSmiles('F[C@H](C)C')
    Chem.AssignStereochemistry(m,1)
    self.failUnless(m.GetAtomWithIdx(1).GetChiralTag() == Chem.ChiralType.CHI_UNSPECIFIED)
    self.failIf(m.GetAtomWithIdx(1).HasProp('_CIPCode'))

    m = Chem.MolFromSmiles('F\\C=C/Cl')
    self.failUnless(m.GetBondWithIdx(0).GetStereo()==Chem.BondStereo.STEREONONE)
    self.failUnless(m.GetBondWithIdx(1).GetStereo()==Chem.BondStereo.STEREOZ)
    atoms = m.GetBondWithIdx(1).GetStereoAtoms()
    self.failUnless(0 in atoms)
    self.failUnless(3 in atoms)
    self.failUnless(m.GetBondWithIdx(2).GetStereo()==Chem.BondStereo.STEREONONE)
    Chem.RemoveStereochemistry(m)
    self.failUnless(m.GetBondWithIdx(1).GetStereo()==Chem.BondStereo.STEREONONE)

    
    m = Chem.MolFromSmiles('F\\C=CCl')
    self.failUnless(m.GetBondWithIdx(1).GetStereo()==Chem.BondStereo.STEREONONE)

  def test36SubstructMatchStr(self):
    """ test the _SubstructMatchStr function """
    query = Chem.MolFromSmarts('[n,p]1ccccc1')
    self.failUnless(query)
    mol = Chem.MolFromSmiles('N1=CC=CC=C1')
    self.failUnless(mol.HasSubstructMatch(query))
    self.failUnless(Chem._HasSubstructMatchStr(mol.ToBinary(),query))
    mol = Chem.MolFromSmiles('S1=CC=CC=C1')
    self.failUnless(not Chem._HasSubstructMatchStr(mol.ToBinary(),query))
    self.failUnless(not mol.HasSubstructMatch(query))
    mol = Chem.MolFromSmiles('P1=CC=CC=C1')
    self.failUnless(mol.HasSubstructMatch(query))
    self.failUnless(Chem._HasSubstructMatchStr(mol.ToBinary(),query))

    
  def test37SanitException(self):
    mol = Chem.MolFromSmiles('CC(C)(C)(C)C',0)
    self.failUnless(mol)
    self.failUnlessRaises(ValueError,lambda:Chem.SanitizeMol(mol))

  def test38TDTSuppliers(self):
    data="""$SMI<Cc1nnc(N)nc1C>
CAS<17584-12-2>
|
$SMI<Cc1n[nH]c(=O)nc1N>
CAS<~>
|
$SMI<Cc1n[nH]c(=O)[nH]c1=O>
CAS<932-53-6>
|
$SMI<Cc1nnc(NN)nc1O>
CAS<~>
|"""
    suppl = Chem.TDTMolSupplier()
    suppl.SetData(data,"CAS")
    i=0;
    for mol in suppl:
      self.failUnless(mol)
      self.failUnless(mol.GetNumAtoms())
      self.failUnless(mol.HasProp("CAS"))
      self.failUnless(mol.HasProp("_Name"))
      self.failUnless(mol.GetProp("CAS")==mol.GetProp("_Name"))
      self.failUnless(mol.GetNumConformers()==0)
      i+=1
    self.failUnless(i==4)
    self.failUnless(len(suppl)==4)

  def test38Issue266(self):
    """ test issue 266: generation of kekulized smiles"""
    mol = Chem.MolFromSmiles('c1ccccc1')
    Chem.Kekulize(mol)
    smi = Chem.MolToSmiles(mol)
    self.failUnless(smi=='c1ccccc1')
    smi = Chem.MolToSmiles(mol,kekuleSmiles=True)
    self.failUnless(smi=='C1=CC=CC=C1')
    
  def test39Issue273(self):
    """ test issue 273: MolFileComments and MolFileInfo props ending up in SD files

    """
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','Wrap',
                                            'test_data','outNCI_few.sdf')
    suppl = Chem.SDMolSupplier(fileN)
    ms = [x for x in suppl]
    for m in ms:
      self.failUnless(m.HasProp('_MolFileInfo'))
      self.failUnless(m.HasProp('_MolFileComments'))
    fName = tempfile.mktemp('.sdf')
    w = Chem.SDWriter(fName)
    w.SetProps(ms[0].GetPropNames())
    for m in ms:
      w.write(m)
    w = None

    txt= file(fName,'r').read()
    os.unlink(fName)
    self.failUnless(txt.find('MolFileInfo')==-1)
    self.failUnless(txt.find('MolFileComments')==-1)
    

  def test40SmilesRootedAtAtom(self):
    """ test the rootAtAtom functionality

    """
    smi = 'CN(C)C'
    m = Chem.MolFromSmiles(smi)

    self.failUnless(Chem.MolToSmiles(m)=='CN(C)C')
    self.failUnless(Chem.MolToSmiles(m,rootedAtAtom=1)=='N(C)(C)C')
    

  def test41SetStreamIndices(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','NCI_aids_few.sdf')
    sdSup = Chem.SDMolSupplier(fileN)
    molNames = ["48", "78", "128", "163", "164", "170", "180", "186",
            "192", "203", "210", "211", "213", "220", "229", "256"]
    indices=[0, 2136, 6198, 8520, 11070, 12292, 14025, 15313, 17313, 20125, 22231,
	     23729, 26147, 28331, 32541, 33991]
    sdSup._SetStreamIndices(indices)
    self.failUnless(len(sdSup) == 16)
    mol = sdSup[5]
    self.failUnless(mol.GetProp("_Name") == "170")
    
    i = 0
    for mol in sdSup :
      self.failUnless(mol)
      self.failUnless(mol.GetProp("_Name") == molNames[i])
      i += 1
          
    ns = [mol.GetProp("_Name") for mol in sdSup]
    self.failUnless(ns == molNames)

    # this can also be used to skip molecules in the file:
    indices=[0, 6198, 12292]
    sdSup._SetStreamIndices(indices)
    self.failUnless(len(sdSup) == 3)
    mol = sdSup[2]
    self.failUnless(mol.GetProp("_Name") == "170")

    # or to reorder them:
    indices=[0, 12292, 6198]
    sdSup._SetStreamIndices(indices)
    self.failUnless(len(sdSup) == 3)
    mol = sdSup[1]
    self.failUnless(mol.GetProp("_Name") == "170")

  def test42LifeTheUniverseAndEverything(self) :
    self.failUnless(True)
    
  def test43TplFileParsing(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','cmpd2.tpl')
    m1 = Chem.MolFromTPLFile(fileN)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==12)
    self.failUnless(m1.GetNumConformers()==2)
    
    m1 = Chem.MolFromTPLFile(fileN,skipFirstConf=True)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==12)
    self.failUnless(m1.GetNumConformers()==1)

    block = file(fileN,'r').read()
    m1 = Chem.MolFromTPLBlock(block)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==12)
    self.failUnless(m1.GetNumConformers()==2)
    
  def test44TplFileWriting(self) :
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','cmpd2.tpl')
    m1 = Chem.MolFromTPLFile(fileN)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==12)
    self.failUnless(m1.GetNumConformers()==2)

    block = Chem.MolToTPLBlock(m1)
    m1 = Chem.MolFromTPLBlock(block)
    self.failUnless(m1 is not None)
    self.failUnless(m1.GetNumAtoms()==12)
    self.failUnless(m1.GetNumConformers()==2)

  def test45RingInfo(self):
    """ test the RingInfo class

    """
    smi = 'CNC'
    m = Chem.MolFromSmiles(smi)
    ri = m.GetRingInfo()
    self.failUnless(ri)
    self.failUnless(ri.NumRings()==0)
    self.failIf(ri.IsAtomInRingOfSize(0,3))
    self.failIf(ri.IsAtomInRingOfSize(1,3))
    self.failIf(ri.IsAtomInRingOfSize(2,3))
    self.failIf(ri.IsBondInRingOfSize(1,3))
    self.failIf(ri.IsBondInRingOfSize(2,3))

    smi = 'C1CC2C1C2'
    m = Chem.MolFromSmiles(smi)
    ri = m.GetRingInfo()
    self.failUnless(ri)
    self.failUnless(ri.NumRings()==2)
    self.failIf(ri.IsAtomInRingOfSize(0,3))
    self.failUnless(ri.IsAtomInRingOfSize(0,4))
    self.failIf(ri.IsBondInRingOfSize(0,3))
    self.failUnless(ri.IsBondInRingOfSize(0,4))
    self.failUnless(ri.IsAtomInRingOfSize(2,4))
    self.failUnless(ri.IsAtomInRingOfSize(2,3))
    self.failUnless(ri.IsBondInRingOfSize(2,3))
    self.failUnless(ri.IsBondInRingOfSize(2,4))

  def test47RWMols(self):
    """ test the RWMol class

    """
    mol = Chem.MolFromSmiles('C1CCC1')
    self.failUnless(type(mol)==Chem.Mol)
    
    rwmol = Chem.EditableMol(mol)
    self.failUnless(type(rwmol)==Chem.EditableMol)
    newAt = Chem.Atom(8)
    rwmol.ReplaceAtom(0,newAt)
    self.failUnless(Chem.MolToSmiles(rwmol.GetMol())=='C1COC1')

    rwmol.RemoveBond(0,1)
    self.failUnless(Chem.MolToSmiles(rwmol.GetMol())=='CCCO')
    a = Chem.Atom(7)
    rwmol.AddAtom(a)
    self.failUnless(rwmol.GetMol().GetNumAtoms()==5)
    rwmol.AddBond(0,4,order=Chem.BondType.SINGLE)
    self.failUnless(Chem.MolToSmiles(rwmol.GetMol())=='CCCON')
    rwmol.AddBond(4,1,order=Chem.BondType.SINGLE)
    self.failUnless(Chem.MolToSmiles(rwmol.GetMol())=='C1CNOC1')
    
    rwmol.RemoveAtom(3)
    self.failUnless(Chem.MolToSmiles(rwmol.GetMol())=='CCNO')
    
    # practice shooting ourselves in the foot:
    m = Chem.MolFromSmiles('c1ccccc1')
    em=Chem.EditableMol(m)
    em.RemoveAtom(0)
    m2 = em.GetMol()
    self.failUnlessRaises(ValueError,lambda : Chem.SanitizeMol(m2))
    m = Chem.MolFromSmiles('c1ccccc1')
    em=Chem.EditableMol(m)
    em.RemoveBond(0,1)
    m2 = em.GetMol()
    self.failUnlessRaises(ValueError,lambda : Chem.SanitizeMol(m2))
                    
    # boundary cases: 
    
    # removing non-existent bonds:
    m = Chem.MolFromSmiles('c1ccccc1')
    em=Chem.EditableMol(m)
    em.RemoveBond(0,2)
    m2 = em.GetMol()
    Chem.SanitizeMol(m2)
    self.failUnless(Chem.MolToSmiles(m2)=='c1ccccc1')
    
    # removing non-existent atoms:
    m = Chem.MolFromSmiles('c1ccccc1')
    em=Chem.EditableMol(m)
    self.failUnlessRaises(RuntimeError,lambda:em.RemoveAtom(12))

  def test47SmartsPieces(self):
    """ test the GetAtomSmarts and GetBondSmarts functions

    """
    m =Chem.MolFromSmarts("[C,N]C")
    self.failUnless(m.GetAtomWithIdx(0).GetSmarts()=='[C,N]')
    self.failUnless(m.GetAtomWithIdx(1).GetSmarts()=='C')
    self.failUnless(m.GetBondBetweenAtoms(0,1).GetSmarts()=='-,:')
    
    m =Chem.MolFromSmarts("[$(C=O)]-O")
    self.failUnless(m.GetAtomWithIdx(0).GetSmarts()=='[$(C=O)]')
    self.failUnless(m.GetAtomWithIdx(1).GetSmarts()=='O')
    self.failUnless(m.GetBondBetweenAtoms(0,1).GetSmarts()=='-')

    m =Chem.MolFromSmiles("CO")
    self.failUnless(m.GetAtomWithIdx(0).GetSmarts()=='C')
    self.failUnless(m.GetAtomWithIdx(1).GetSmarts()=='O')
    self.failUnless(m.GetBondBetweenAtoms(0,1).GetSmarts()=='')

    m =Chem.MolFromSmiles("C=O")
    self.failUnless(m.GetAtomWithIdx(0).GetSmarts()=='C')
    self.failUnless(m.GetAtomWithIdx(1).GetSmarts()=='O')
    self.failUnless(m.GetBondBetweenAtoms(0,1).GetSmarts()=='=')

  def test48Issue1928819(self):
    """ test a crash involving looping directly over mol suppliers
    """
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','NCI_aids_few.sdf')
    ms = [x for x in Chem.SDMolSupplier(fileN)]
    self.failUnless(len(ms)==16)
    count=0
    for m in Chem.SDMolSupplier(fileN): count+=1
    self.failUnless(count==16)

    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','fewSmi.csv')
    count=0
    for m in Chem.SmilesMolSupplier(fileN,titleLine=False,smilesColumn=1): count+=1
    self.failUnless(count==10)
    
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','acd_few.tdt')
    count=0
    for m in Chem.TDTMolSupplier(fileN): count+=1
    self.failUnless(count==10)

  def test49Issue1932365(self):
    """ test aromatic Se and Te from smiles/smarts
    """
    m = Chem.MolFromSmiles('c1ccc[se]1')
    self.failUnless(m)
    self.failUnless(m.GetAtomWithIdx(0).GetIsAromatic())
    self.failUnless(m.GetAtomWithIdx(4).GetIsAromatic())
    m = Chem.MolFromSmiles('c1ccc[te]1')
    self.failUnless(m)
    self.failUnless(m.GetAtomWithIdx(0).GetIsAromatic())
    self.failUnless(m.GetAtomWithIdx(4).GetIsAromatic())
    m = Chem.MolFromSmiles('C1=C[Se]C=C1')
    self.failUnless(m)
    self.failUnless(m.GetAtomWithIdx(0).GetIsAromatic())
    self.failUnless(m.GetAtomWithIdx(2).GetIsAromatic())
    m = Chem.MolFromSmiles('C1=C[Te]C=C1')
    self.failUnless(m)
    self.failUnless(m.GetAtomWithIdx(0).GetIsAromatic())
    self.failUnless(m.GetAtomWithIdx(2).GetIsAromatic())

    p = Chem.MolFromSmarts('[se]')
    self.failUnless(Chem.MolFromSmiles('c1ccc[se]1').HasSubstructMatch(p))
    self.failIf(Chem.MolFromSmiles('C1=CCC[Se]1').HasSubstructMatch(p))
    
    p = Chem.MolFromSmarts('[te]')
    self.failUnless(Chem.MolFromSmiles('c1ccc[te]1').HasSubstructMatch(p))
    self.failIf(Chem.MolFromSmiles('C1=CCC[Te]1').HasSubstructMatch(p))

  def test50Issue1968608(self):
    """ test sf.net issue 1968608
    """
    smarts = Chem.MolFromSmarts("[r5]")
    mol = Chem.MolFromSmiles("N12CCC36C1CC(C(C2)=CCOC4CC5=O)C4C3N5c7ccccc76")
    count = len(mol.GetSubstructMatches(smarts, uniquify=0))
    self.failUnless(count==9)

  def test51RadicalHandling(self):
    """ test handling of atoms with radicals
    """
    mol = Chem.MolFromSmiles("[C]C")
    self.failUnless(mol)
    atom=mol.GetAtomWithIdx(0)
    self.failUnless(atom.GetNumRadicalElectrons()==3)
    self.failUnless(atom.GetNoImplicit())
    atom.SetNoImplicit(False)
    atom.SetNumRadicalElectrons(1)
    mol.UpdatePropertyCache()
    self.failUnless(atom.GetNumRadicalElectrons()==1)
    self.failUnless(atom.GetNumImplicitHs()==2)
    
    mol = Chem.MolFromSmiles("[c]1ccccc1")
    self.failUnless(mol)
    atom=mol.GetAtomWithIdx(0)
    self.failUnless(atom.GetNumRadicalElectrons()==1)
    self.failUnless(atom.GetNoImplicit())

    mol = Chem.MolFromSmiles("[n]1ccccc1")
    self.failUnless(mol)
    atom=mol.GetAtomWithIdx(0)
    self.failUnless(atom.GetNumRadicalElectrons()==0)
    self.failUnless(atom.GetNoImplicit())


  def test52MolFrags(self):
    """ test GetMolFrags functionality
    """
    mol = Chem.MolFromSmiles("C.CC")
    self.failUnless(mol)
    fs = Chem.GetMolFrags(mol)
    self.failUnless(len(fs)==2)
    self.failUnless(len(fs[0])==1)
    self.failUnless(tuple(fs[0])==(0,))
    self.failUnless(len(fs[1])==2)
    self.failUnless(tuple(fs[1])==(1,2))

    fs = Chem.GetMolFrags(mol,True)
    self.failUnless(len(fs)==2)
    self.failUnless(fs[0].GetNumAtoms()==1)
    self.failUnless(fs[1].GetNumAtoms()==2)
    
    mol = Chem.MolFromSmiles("CCC")
    self.failUnless(mol)
    fs = Chem.GetMolFrags(mol)
    self.failUnless(len(fs)==1)
    self.failUnless(len(fs[0])==3)
    self.failUnless(tuple(fs[0])==(0,1,2))
    fs = Chem.GetMolFrags(mol,True)
    self.failUnless(len(fs)==1)
    self.failUnless(fs[0].GetNumAtoms()==3)

  def test53Matrices(self) :
    """ test adjacency and distance matrices
       
    """ 
    m = Chem.MolFromSmiles('CC=C')
    d = Chem.GetDistanceMatrix(m,0)
    self.failUnless(feq(d[0,1],1.0))
    self.failUnless(feq(d[0,2],2.0))
    self.failUnless(feq(d[1,0],1.0))
    self.failUnless(feq(d[2,0],2.0))
    a = Chem.GetAdjacencyMatrix(m,0)
    self.failUnless(a[0,1]==1)
    self.failUnless(a[0,2]==0)
    self.failUnless(a[1,2]==1)
    self.failUnless(a[1,0]==1)
    self.failUnless(a[2,0]==0)

    m = Chem.MolFromSmiles('C1CC1')
    d = Chem.GetDistanceMatrix(m,0)
    self.failUnless(feq(d[0,1],1.0))
    self.failUnless(feq(d[0,2],1.0))
    a = Chem.GetAdjacencyMatrix(m,0)
    self.failUnless(a[0,1]==1)
    self.failUnless(a[0,2]==1)
    self.failUnless(a[1,2]==1)

    m = Chem.MolFromSmiles('CC.C')
    d = Chem.GetDistanceMatrix(m,0)
    self.failUnless(feq(d[0,1],1.0))
    self.failUnless(d[0,2]>1000)
    self.failUnless(d[1,2]>1000)
    a = Chem.GetAdjacencyMatrix(m,0)
    self.failUnless(a[0,1]==1)
    self.failUnless(a[0,2]==0)
    self.failUnless(a[1,2]==0)

  def test54Mol2Parser(self):
    """ test the mol2 parser
    """
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','pyrazole_pyridine.mol2')
    m = Chem.MolFromMol2File(fileN)
    self.failUnless(m.GetNumAtoms()==5)
    self.failUnless(Chem.MolToSmiles(m)=='c1cn[nH]c1',Chem.MolToSmiles(m))


  def test56LazySDMolSupplier(self) :
    if not hasattr(Chem,'CompressedSDMolSupplier'): return
    fileN = os.path.join(RDConfig.RDBaseDir,'Code','GraphMol','FileParsers',
                                            'test_data','NCI_aids_few.sdf.gz')
    sdSup = Chem.CompressedSDMolSupplier(fileN)
    molNames = ["48", "78", "128", "163", "164", "170", "180", "186",
            "192", "203", "210", "211", "213", "220", "229", "256"]

    chgs192 = {8:1, 11:1, 15:-1, 18:-1, 20:1, 21:1, 23:-1, 25:-1} 
    i = 0
    for mol in sdSup :
      self.failUnless(mol)
      self.failUnless(mol.GetProp("_Name") == molNames[i])
      i += 1
      if (mol.GetProp("_Name") == "192") :
        # test parsed charges on one of the molecules
        for id in chgs192.keys() :
          self.failUnless(mol.GetAtomWithIdx(id).GetFormalCharge() == chgs192[id])
    self.failUnlessEqual(i,16)
          
    sdSup = Chem.CompressedSDMolSupplier(fileN)
    ns = [mol.GetProp("_Name") for mol in sdSup]
    self.failUnless(ns == molNames)

    sdSup = Chem.CompressedSDMolSupplier(fileN, 0)
    for mol in sdSup :
      self.failUnless(not mol.HasProp("numArom"))

  def test57AddRecursiveQuery(self):
    q1 = Chem.MolFromSmiles('CC')
    q2 = Chem.MolFromSmiles('CO')
    Chem.AddRecursiveQuery(q1,q2,1)

    m1 = Chem.MolFromSmiles('OCC')
    self.failUnless(m1.HasSubstructMatch(q2))
    self.failUnless(m1.HasSubstructMatch(q1))
    self.failUnless(m1.HasSubstructMatch(q1))
    self.failUnless(m1.GetSubstructMatch(q1)==(2,1))

    q3 = Chem.MolFromSmiles('CS')
    Chem.AddRecursiveQuery(q1,q3,1)
    
    self.failIf(m1.HasSubstructMatch(q3))
    self.failIf(m1.HasSubstructMatch(q1))

    m2 = Chem.MolFromSmiles('OC(S)C')
    self.failUnless(m2.HasSubstructMatch(q1))
    self.failUnless(m2.GetSubstructMatch(q1)==(3,1))
    
    m3 = Chem.MolFromSmiles('SCC')
    self.failUnless(m3.HasSubstructMatch(q3))
    self.failIf(m3.HasSubstructMatch(q1))

    q1 = Chem.MolFromSmiles('CC')
    Chem.AddRecursiveQuery(q1,q2,1)
    Chem.AddRecursiveQuery(q1,q3,1,False)
    self.failUnless(m3.HasSubstructMatch(q1))
    self.failUnless(m3.GetSubstructMatch(q1)==(2,1))
    
if __name__ == '__main__':
  unittest.main()

