#ifndef MY_TEMPLATE_SHAPE
#define MY_TEMPLATE_SHAPE

#include "Riostream.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "TH1F.h"
#include "TFile.h"
#include "TString.h"
#include <vector>

class MyTemplateShape : public RooAbsPdf {

public:
  MyTemplateShape() {} ; 
  MyTemplateShape(const char *name, const char *title,
		  RooAbsReal& _m, RooAbsReal& _pt, RooAbsReal& _eta, RooAbsReal& _isPassing,
		  char* genfile = "MCtemplates.root"
		  );
  
  MyTemplateShape(const MyTemplateShape& other, const char* name);
  inline virtual TObject* clone(const char* newname) const { return new MyTemplateShape(*this,newname);}
  inline ~MyTemplateShape(){};
  ClassDef(MyTemplateShape,1)
  Double_t evaluate() const;  
 protected:
  RooRealProxy m ;
  RooRealProxy pt ;
  RooRealProxy eta ;
  RooRealProxy isPassing ;
  RooDataHist* dataHist[50][50][2];
  int Choose_pt_bin(Double_t thispt) const;
  int Choose_eta_bin(Double_t thiseta) const;
  std::vector<float> ptcuts;
  std::vector<float> etacuts;
};

#endif
