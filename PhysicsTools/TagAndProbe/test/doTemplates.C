#define doTemplates_cxx
#include "doTemplates.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TFile.h"
#include "TH1F.h"
#include "TString.h"
#include <vector>

void doTemplates::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L doTemplates.C
//      Root > doTemplates t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   TH1F *histos_pass[50][50];
   TH1F *histos_fail[50][50];

   for (unsigned int i=0; i<ptcuts.size()-1; i++) for (unsigned int j=0; j<etacuts.size()-1; j++) histos_pass[i][j] = new TH1F(Form("Mass_templatehisto_pt%d_eta%d_pass",i,j),Form("Mass_templatehisto_pt%d_eta%d_pass",i,j),160,70,110);
   for (unsigned int i=0; i<ptcuts.size()-1; i++) for (unsigned int j=0; j<etacuts.size()-1; j++) histos_fail[i][j] = new TH1F(Form("Mass_templatehisto_pt%d_eta%d_fail",i,j),Form("Mass_templatehisto_pt%d_eta%d_fail",i,j),160,70,110);

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      if (Cut(ientry) < 0) continue;


      int ptbin = Choose_pt_bin(probe_pt);
      int etabin = Choose_eta_bin(probe_eta);

      if (ptbin<0 || etabin<0) continue;
      if (mass<70 || mass>110) continue;

      if (*probe_passing) histos_pass[ptbin][etabin]->Fill(mass,PUweight);
      else histos_fail[ptbin][etabin]->Fill(mass,PUweight);

   }

   TFile *f = new TFile("MCtemplates.root","recreate");
   f->cd();
   for (unsigned int i=0; i<ptcuts.size()-1; i++) for (unsigned int j=0; j<etacuts.size()-1; j++) histos_pass[i][j]->Write();
   for (unsigned int i=0; i<ptcuts.size()-1; i++) for (unsigned int j=0; j<etacuts.size()-1; j++) histos_fail[i][j]->Write();
   f->Close();


}


int doTemplates::Choose_pt_bin(Double_t thispt) const{
  unsigned int size = ptcuts.size();
  if (thispt<ptcuts.at(0)) return -1;
  if (thispt>=ptcuts.at(size-1)) return -1;
  for (unsigned int i=0; i<size-1; i++) if (thispt>=ptcuts.at(i) && thispt<ptcuts.at(i+1)) return (int)i;
  return -1;
}

int doTemplates::Choose_eta_bin(Double_t thiseta) const{
  thiseta = fabs(thiseta);
  unsigned int size = etacuts.size();
  if (thiseta<etacuts.at(0)) return -1;
  if (thiseta>=etacuts.at(size-1)) return -1;
  for (unsigned int i=0; i<size-1; i++) if (thiseta>=etacuts.at(i) && thiseta<etacuts.at(i+1)) return (int)i;
  return -1;
}








