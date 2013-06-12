// -*- C++ -*-
//
// Package:    PileupWeightProducer
// Class:      PileupWeightProducer
// 
/**\class PileupWeightProducer PileupWeightProducer.cc 

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <vector>

#include "TFile.h"
#include "TH1F.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

//
// class declaration
//

class PileupWeightProducer : public edm::EDProducer {
   public:
      explicit PileupWeightProducer(const edm::ParameterSet&);
      ~PileupWeightProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
   // ----------member data ---------------------------
   std::string pileupData_;
   std::string pileupMC_;
   TFile* dataFile_;
   TFile* mcFile_;
   TH1F* h_pileupData_;
   TH1F* h_pileupMC_;
   TH1F* h_pileupRatio_;

};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
PileupWeightProducer::PileupWeightProducer(const edm::ParameterSet& iConfig)
{

  
  pileupData_ = iConfig.getUntrackedParameter<std::string>("PileupDataFile");
  TFile* dataFile_ = new TFile(pileupData_.c_str(), "READ");
  h_pileupData_ = new TH1F(  *(static_cast<TH1F*>(dataFile_->Get( "pileup" )->Clone() )) );

  h_pileupData_->Print();

  pileupMC_ = iConfig.getUntrackedParameter<std::string>("PileupMCFile");
  TFile* mcFile_ = new TFile(pileupMC_.c_str(), "READ");
  h_pileupMC_ = new TH1F(  *(static_cast<TH1F*>(mcFile_->Get( "pileup" )->Clone() )) );
  
  h_pileupMC_->Print();

  h_pileupData_->Scale( 1.0/ h_pileupData_->Integral() );
  h_pileupMC_->Scale( 1.0/ h_pileupMC_->Integral() );
  h_pileupRatio_ = new TH1F( *(h_pileupData_)) ;
  h_pileupRatio_->Divide(h_pileupMC_);
  
  //register your products
  
  produces<std::vector<float> >( "pileupWeights" ).setBranchAlias( "pileupWeights" );

}


PileupWeightProducer::~PileupWeightProducer()
{
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)
  delete h_pileupData_;
  delete h_pileupMC_;
  delete h_pileupRatio_;
//   dataFile_ -> Close();
//   delete dataFile_;
}

// ------------ method called to produce the data  ------------
void
PileupWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   using namespace edm;
   std::auto_ptr<std::vector<float> > pileupWeights( new std::vector<float> );

   edm::Handle<reco::VertexCollection> recVtxs;
   iEvent.getByLabel("offlinePrimaryVertices",recVtxs);
   int mNPV_ = 0;

   for(unsigned int ind=0;ind<recVtxs->size();ind++) {
     if (!((*recVtxs)[ind].isFake()) && ((*recVtxs)[ind].ndof()>4) 
	 && (fabs((*recVtxs)[ind].z())<=24.0) &&  
	 ((*recVtxs)[ind].position().Rho()<=2.0) ) {
       mNPV_++;
     }
   }

   float nominalWeight = h_pileupRatio_->GetBinContent(int(mNPV_+0.01)+1); 
   pileupWeights->push_back( nominalWeight );

   iEvent.put(pileupWeights, "pileupWeights");

}

// ------------ method called once each job just before starting event loop  ------------
void 
PileupWeightProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PileupWeightProducer::endJob() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PileupWeightProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PileupWeightProducer);
