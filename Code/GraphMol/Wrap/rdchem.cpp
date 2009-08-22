// $Id$
//
//  Copyright (C) 2003-2006 Rational Discovery LLC
//
//   @@ All Rights Reserved  @@
//
#include <RDBoost/Wrap.h>
#include "rdchem.h"
#include <GraphMol/RDKitBase.h>
#include <GraphMol/SanitException.h>

#include <sstream>

#include "seqs.hpp"
namespace python = boost::python;
using namespace RDKit;


namespace RDKit{
  void tossit(){
    throw IndexErrorException(1);
  }
}

void rdExceptionTranslator(RDKit::ConformerException const& x){
  PyErr_SetString(PyExc_ValueError,"Bad Conformer Id");
}

void rdSanitExceptionTranslator(RDKit::MolSanitizeException const& x){
  std::ostringstream ss;
  ss << "Sanitization error: " << x.message();
  PyErr_SetString(PyExc_ValueError,ss.str().c_str());
}

void wrap_table();
void wrap_atom();
void wrap_conformer();
void wrap_bond();
void wrap_mol();
void wrap_ringinfo();
void wrap_EditableMol();

BOOST_PYTHON_MODULE(rdchem)
{

  python::scope().attr("__doc__") =
    "Module containing the core chemistry functionality of the RDKit"
    ;
  RegisterListConverter<RDKit::Atom*>();
  RegisterListConverter<RDKit::Bond*>();
  python::register_exception_translator<IndexErrorException>(&translate_index_error);
  python::register_exception_translator<ValueErrorException>(&translate_value_error);
  python::register_exception_translator<RDKit::MolSanitizeException>(&rdSanitExceptionTranslator);


  //*********************************************
  //
  //  Utility Classes
  //
  //*********************************************
  python::class_< AtomIterSeq >("_ROAtomSeq",
				"Read-only sequence of atoms, not constructable from Python.",
				python::no_init)
    .def("__len__",&AtomIterSeq::len)
    .def("__getitem__",&AtomIterSeq::get_item,
	 python::return_value_policy<python::reference_existing_object>())
    ;
  python::class_< BondIterSeq >("_ROBondSeq",
				"Read-only sequence of bonds, not constructable from Python.",
				python::no_init)
    // FIX: we ought to be able to expose an iteration interface
    .def("__len__",&BondIterSeq::len)
    .def("__getitem__",&BondIterSeq::get_item,
	 python::return_value_policy<python::reference_existing_object>())
    ;


  //*********************************************
  //
  //  Classes
  //
  //*********************************************
  wrap_table();
  wrap_atom();
  wrap_conformer();
  wrap_bond();
  wrap_mol();
  wrap_EditableMol();
  wrap_ringinfo();

  //*********************************************
  //
  //  Functions
  //
  //*********************************************

  std::string docString;

  python::def("tossit",tossit);

}


