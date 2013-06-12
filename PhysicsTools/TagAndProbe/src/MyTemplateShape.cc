#include "PhysicsTools/TagAndProbe/interface/MyTemplateShape.h"

ClassImp(MyTemplateShape)

MyTemplateShape::MyTemplateShape(const char *name, const char *title,
				 RooAbsReal& _m, RooAbsReal& _pt, RooAbsReal& _eta, RooAbsReal& _isPassing,
				 char* genfile
				 ): 
  RooAbsPdf(name,title),
  m("m","m", this,_m),  
  pt("pt","pt", this,_pt),  
  eta("eta","eta", this,_eta),
  isPassing("isPassing","isPassing", this,_isPassing)
{

  TFile *f_gen= TFile::Open(genfile);
  for (int i=0; i<50; i++)
    for (int j=0; j<50; j++){
      dataHist[i][j][0]=0;
      dataHist[i][j][1]=0;
    }

#include "PhysicsTools/TagAndProbe/interface/bins.h"

  ptcuts=std::vector<float>(myptcuts,myptcuts+sizeof(myptcuts)/sizeof(float));
  etacuts=std::vector<float>(myetacuts,myetacuts+sizeof(myetacuts)/sizeof(float));

  for (unsigned int i=0; i<ptcuts.size()-1; i++)
    for (unsigned int j=0; j<etacuts.size()-1; j++){
    TH1F* mass_th1f_pass = (TH1F*)  f_gen->Get(Form("Mass_templatehisto_pt%d_eta%d_pass",i,j));
    TH1F* mass_th1f_fail = (TH1F*)  f_gen->Get(Form("Mass_templatehisto_pt%d_eta%d_fail",i,j));
    dataHist[i][j][0] = new RooDataHist(Form("Mass_templ_pt%d_eta%d_pass",i,j), Form("Mass_templ_pt%d_eta%d_pass",i,j), _m, mass_th1f_pass );
    dataHist[i][j][1] = new RooDataHist(Form("Mass_templ_pt%d_eta%d_fail",i,j), Form("Mass_templ_pt%d_eta%d_fail",i,j), _m, mass_th1f_fail );
//    dataHist[i][j][0]->Print();
//    dataHist[i][j][1]->Print();
  }
  f_gen->Close();


}


MyTemplateShape::MyTemplateShape(const MyTemplateShape& other, const char* name):
  RooAbsPdf(other,name),
  m("m", this,other.m),
  pt("pt", this,other.pt),
  eta("eta", this,other.eta),
  isPassing("isPassing", this,other.isPassing)
{
  for (int i=0;i<50; i++) for (int j=0; j<50; j++) for (int k=0; k<2; k++) dataHist[i][j][k]=other.dataHist[i][j][k];
  ptcuts=other.ptcuts;
  etacuts=other.etacuts;
}


Double_t MyTemplateShape::evaluate() const{

  int pt_bin = Choose_pt_bin(pt.arg().getVal());
  int eta_bin = Choose_eta_bin(eta.arg().getVal());

  if (pt_bin<0 || eta_bin<0) return 0;

  return (isPassing.arg().getVal()>0.5) ? dataHist[pt_bin][eta_bin][0]->weight(m.arg()) : dataHist[pt_bin][eta_bin][1]->weight(m.arg());

}

int MyTemplateShape::Choose_pt_bin(Double_t thispt) const{
  unsigned int size = ptcuts.size();
  if (thispt<ptcuts.at(0)) return -1;
  if (thispt>=ptcuts.at(size-1)) return -1;
  for (unsigned int i=0; i<size-1; i++) if (thispt>=ptcuts.at(i) && thispt<ptcuts.at(i+1)) return (int)i;
  return -1;
}

int MyTemplateShape::Choose_eta_bin(Double_t thiseta) const{
  thiseta = fabs(thiseta);
  unsigned int size = etacuts.size();
  if (thiseta<etacuts.at(0)) return -1;
  if (thiseta>=etacuts.at(size-1)) return -1;
  for (unsigned int i=0; i<size-1; i++) if (thiseta>=etacuts.at(i) && thiseta<etacuts.at(i+1)) return (int)i;
  return -1;
}
