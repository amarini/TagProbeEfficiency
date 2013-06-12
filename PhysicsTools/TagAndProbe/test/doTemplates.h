//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Jun 12 15:30:29 2013 by ROOT version 5.27/06b
// from TTree fitter_tree/fitter_tree
// found on file: Photon_tagProbeTree_Zee_mc.root
//////////////////////////////////////////////////////////

#ifndef doTemplates_h
#define doTemplates_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "TH1F.h"
#include "TString.h"
#include <vector>
#include <assert.h>

class doTemplates {
public :


   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Float_t         probe_ecalRecHitSumEtConeDR03;
   Float_t         probe_eta;
   Float_t         probe_hadronicOverEm;
   Float_t         probe_hasPixelSeed;
   Float_t         probe_hcalTowerSumEtConeDR03;
   Float_t         probe_phi;
   Float_t         probe_pt;
   Float_t         probe_sc_energy;
   Float_t         probe_sc_et;
   Float_t         probe_sc_eta;
   Float_t         probe_sc_phi;
   Float_t         probe_sigmaIetaIeta_NOTSCALED;
   Float_t         probe_trkSumPtHollowConeDR03;
   Int_t           probe_passingPhotonID;
   Int_t           probe_passingPixelVeto;
   Float_t         PUweight;
   UInt_t          run;
   UInt_t          lumi;
   UInt_t          event;
   Int_t           event_nPV;
   Float_t         event_met_calomet;
   Float_t         event_met_calosumet;
   Float_t         event_met_calometsignificance;
   Float_t         event_met_tcmet;
   Float_t         event_met_tcsumet;
   Float_t         event_met_tcmetsignificance;
   Float_t         event_met_pfmet;
   Float_t         event_met_pfsumet;
   Float_t         event_met_pfmetsignificance;
   Float_t         event_PrimaryVertex_x;
   Float_t         event_PrimaryVertex_y;
   Float_t         event_PrimaryVertex_z;
   Float_t         event_BeamSpot_x;
   Float_t         event_BeamSpot_y;
   Float_t         event_BeamSpot_z;
   Float_t         mass;
   Int_t           mcTrue;
   Float_t         mcMass;
   Float_t         tag_eta;
   Float_t         tag_phi;
   Float_t         tag_pt;
   Float_t         mc_probe_eta;
   Float_t         mc_probe_phi;
   Float_t         mc_probe_pt;
   Float_t         pair_eta;
   Float_t         pair_mass;
   Float_t         pair_phi;
   Float_t         pair_pt;

   // List of branches
   TBranch        *b_probe_ecalRecHitSumEtConeDR03;   //!
   TBranch        *b_probe_eta;   //!
   TBranch        *b_probe_hadronicOverEm;   //!
   TBranch        *b_probe_hasPixelSeed;   //!
   TBranch        *b_probe_hcalTowerSumEtConeDR03;   //!
   TBranch        *b_probe_phi;   //!
   TBranch        *b_probe_pt;   //!
   TBranch        *b_probe_sc_energy;   //!
   TBranch        *b_probe_sc_et;   //!
   TBranch        *b_probe_sc_eta;   //!
   TBranch        *b_probe_sc_phi;   //!
   TBranch        *b_probe_sigmaIetaIeta_NOTSCALED;   //!
   TBranch        *b_probe_trkSumPtHollowConeDR03;   //!
   TBranch        *b_probe_passingPhotonID;   //!
   TBranch        *b_probe_passingPixelVeto;   //!
   TBranch        *b_PUweight;   //!
   TBranch        *b_run;   //!
   TBranch        *b_lumi;   //!
   TBranch        *b_event;   //!
   TBranch        *b_mNPV;   //!
   TBranch        *b_mMET;   //!
   TBranch        *b_mSumET;   //!
   TBranch        *b_mMETSign;   //!
   TBranch        *b_mtcMET;   //!
   TBranch        *b_mtcSumET;   //!
   TBranch        *b_mtcMETSign;   //!
   TBranch        *b_mpfMET;   //!
   TBranch        *b_mpfSumET;   //!
   TBranch        *b_mpfMETSign;   //!
   TBranch        *b_mPVx;   //!
   TBranch        *b_mPVy;   //!
   TBranch        *b_mPVz;   //!
   TBranch        *b_mBSx;   //!
   TBranch        *b_mBSy;   //!
   TBranch        *b_mBSz;   //!
   TBranch        *b_mass;   //!
   TBranch        *b_mcTrue;   //!
   TBranch        *b_mcMass;   //!
   TBranch        *b_tag_eta;   //!
   TBranch        *b_tag_phi;   //!
   TBranch        *b_tag_pt;   //!
   TBranch        *b_mc_probe_eta;   //!
   TBranch        *b_mc_probe_phi;   //!
   TBranch        *b_mc_probe_pt;   //!
   TBranch        *b_pair_eta;   //!
   TBranch        *b_pair_mass;   //!
   TBranch        *b_pair_phi;   //!
   TBranch        *b_pair_pt;   //!

   doTemplates(bool isZuug=false);
   virtual ~doTemplates();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);

   std::vector<float> ptcuts;
   std::vector<float> etacuts;

   int Choose_pt_bin(Double_t thispt) const;
   int Choose_eta_bin(Double_t thiseta) const;

   Int_t *probe_passing;

};

#endif

#ifdef doTemplates_cxx
doTemplates::doTemplates(bool isZuug)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.


  TTree *tree = NULL;
  tree = (TTree*)(gDirectory->Get("PhotonToIsoId/fitter_tree"));
  assert (tree!=NULL);

   Init(tree);

#include "../interface/bins.h"

   ptcuts=std::vector<float>(myptcuts,myptcuts+sizeof(myptcuts)/sizeof(float));
   etacuts=std::vector<float>(myetacuts,myetacuts+sizeof(myetacuts)/sizeof(float));

   if (!isZuug) probe_passing = &probe_passingPhotonID; else probe_passing = &probe_passingPixelVeto; 

}

doTemplates::~doTemplates()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t doTemplates::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t doTemplates::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (!fChain->InheritsFrom(TChain::Class()))  return centry;
   TChain *chain = (TChain*)fChain;
   if (chain->GetTreeNumber() != fCurrent) {
      fCurrent = chain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void doTemplates::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("probe_ecalRecHitSumEtConeDR03", &probe_ecalRecHitSumEtConeDR03, &b_probe_ecalRecHitSumEtConeDR03);
   fChain->SetBranchAddress("probe_eta", &probe_eta, &b_probe_eta);
   fChain->SetBranchAddress("probe_hadronicOverEm", &probe_hadronicOverEm, &b_probe_hadronicOverEm);
   fChain->SetBranchAddress("probe_hasPixelSeed", &probe_hasPixelSeed, &b_probe_hasPixelSeed);
   fChain->SetBranchAddress("probe_hcalTowerSumEtConeDR03", &probe_hcalTowerSumEtConeDR03, &b_probe_hcalTowerSumEtConeDR03);
   fChain->SetBranchAddress("probe_phi", &probe_phi, &b_probe_phi);
   fChain->SetBranchAddress("probe_pt", &probe_pt, &b_probe_pt);
   fChain->SetBranchAddress("probe_sc_energy", &probe_sc_energy, &b_probe_sc_energy);
   fChain->SetBranchAddress("probe_sc_et", &probe_sc_et, &b_probe_sc_et);
   fChain->SetBranchAddress("probe_sc_eta", &probe_sc_eta, &b_probe_sc_eta);
   fChain->SetBranchAddress("probe_sc_phi", &probe_sc_phi, &b_probe_sc_phi);
   fChain->SetBranchAddress("probe_sigmaIetaIeta_NOTSCALED", &probe_sigmaIetaIeta_NOTSCALED, &b_probe_sigmaIetaIeta_NOTSCALED);
   fChain->SetBranchAddress("probe_trkSumPtHollowConeDR03", &probe_trkSumPtHollowConeDR03, &b_probe_trkSumPtHollowConeDR03);
   fChain->SetBranchAddress("probe_passingPhotonID", &probe_passingPhotonID, &b_probe_passingPhotonID);
   fChain->SetBranchAddress("probe_passingPixelVeto", &probe_passingPixelVeto, &b_probe_passingPixelVeto);
   fChain->SetBranchAddress("PUweight", &PUweight, &b_PUweight);
   fChain->SetBranchAddress("run", &run, &b_run);
   fChain->SetBranchAddress("lumi", &lumi, &b_lumi);
   fChain->SetBranchAddress("event", &event, &b_event);
   fChain->SetBranchAddress("event_nPV", &event_nPV, &b_mNPV);
   fChain->SetBranchAddress("event_met_calomet", &event_met_calomet, &b_mMET);
   fChain->SetBranchAddress("event_met_calosumet", &event_met_calosumet, &b_mSumET);
   fChain->SetBranchAddress("event_met_calometsignificance", &event_met_calometsignificance, &b_mMETSign);
   fChain->SetBranchAddress("event_met_tcmet", &event_met_tcmet, &b_mtcMET);
   fChain->SetBranchAddress("event_met_tcsumet", &event_met_tcsumet, &b_mtcSumET);
   fChain->SetBranchAddress("event_met_tcmetsignificance", &event_met_tcmetsignificance, &b_mtcMETSign);
   fChain->SetBranchAddress("event_met_pfmet", &event_met_pfmet, &b_mpfMET);
   fChain->SetBranchAddress("event_met_pfsumet", &event_met_pfsumet, &b_mpfSumET);
   fChain->SetBranchAddress("event_met_pfmetsignificance", &event_met_pfmetsignificance, &b_mpfMETSign);
   fChain->SetBranchAddress("event_PrimaryVertex_x", &event_PrimaryVertex_x, &b_mPVx);
   fChain->SetBranchAddress("event_PrimaryVertex_y", &event_PrimaryVertex_y, &b_mPVy);
   fChain->SetBranchAddress("event_PrimaryVertex_z", &event_PrimaryVertex_z, &b_mPVz);
   fChain->SetBranchAddress("event_BeamSpot_x", &event_BeamSpot_x, &b_mBSx);
   fChain->SetBranchAddress("event_BeamSpot_y", &event_BeamSpot_y, &b_mBSy);
   fChain->SetBranchAddress("event_BeamSpot_z", &event_BeamSpot_z, &b_mBSz);
   fChain->SetBranchAddress("mass", &mass, &b_mass);
   fChain->SetBranchAddress("mcTrue", &mcTrue, &b_mcTrue);
   fChain->SetBranchAddress("mcMass", &mcMass, &b_mcMass);
   fChain->SetBranchAddress("tag_eta", &tag_eta, &b_tag_eta);
   fChain->SetBranchAddress("tag_phi", &tag_phi, &b_tag_phi);
   fChain->SetBranchAddress("tag_pt", &tag_pt, &b_tag_pt);
   fChain->SetBranchAddress("mc_probe_eta", &mc_probe_eta, &b_mc_probe_eta);
   fChain->SetBranchAddress("mc_probe_phi", &mc_probe_phi, &b_mc_probe_phi);
   fChain->SetBranchAddress("mc_probe_pt", &mc_probe_pt, &b_mc_probe_pt);
   fChain->SetBranchAddress("pair_eta", &pair_eta, &b_pair_eta);
   fChain->SetBranchAddress("pair_mass", &pair_mass, &b_pair_mass);
   fChain->SetBranchAddress("pair_phi", &pair_phi, &b_pair_phi);
   fChain->SetBranchAddress("pair_pt", &pair_pt, &b_pair_pt);
   Notify();
}

Bool_t doTemplates::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void doTemplates::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t doTemplates::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.

  return mcTrue ? 1 : -1;

  //   return 1;
}
#endif // #ifdef doTemplates_cxx
