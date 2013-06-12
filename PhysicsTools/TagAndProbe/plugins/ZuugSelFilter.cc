#include <iostream>
#include <string>
#include <vector>
#include "PhysicsTools/TagAndProbe/interface/ZuugSelFilter.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgoRcd.h"
#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgo.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "TLorentzVector.h"

using namespace edm;
using namespace reco;
using namespace std;

ZuugSelFilter::ZuugSelFilter(const edm::ParameterSet &params)
{

  src_muons_ = params.getUntrackedParameter<edm::InputTag>("src_muons");
  src_photons_ = params.getUntrackedParameter<edm::InputTag>("src_photons");

  produces< reco::MuonCollection >("ZuugSelMuons");  
  produces< reco::PhotonCollection >("ZuugSelPhotons");  


}




ZuugSelFilter::~ZuugSelFilter()
{

}


//
// member functions
//


// ------------ method called to produce the data  ------------

bool ZuugSelFilter::filter(edm::Event &event, 
			      const edm::EventSetup &eventSetup)
{
   // Create the output collection

  std::auto_ptr< reco::MuonCollection > 
    outColMuon( new reco::MuonCollection );
  std::auto_ptr< reco::PhotonCollection > 
    outColPhoton( new reco::PhotonCollection );


  // Read muons
  Handle<MuonCollection> muons;
  event.getByLabel(src_muons_, muons);

  // Read photons
  Handle<PhotonCollection> photons;
  event.getByLabel(src_photons_, photons);

  // Get the rechits
  edm::Handle< EcalRecHitCollection > pEBRecHits;
  event.getByLabel( "reducedEcalRecHitsEB", pEBRecHits );
  const EcalRecHitCollection *ebRecHits = pEBRecHits.product();
  edm::Handle< EcalRecHitCollection > pEERecHits;
  event.getByLabel( "reducedEcalRecHitsEE", pEERecHits );
  const EcalRecHitCollection *eeRecHits = pEERecHits.product();


  // Get the severity level object
  edm::ESHandle<EcalSeverityLevelAlgo> sevLv;
  eventSetup.get<EcalSeverityLevelAlgoRcd>().get(sevLv);

  // Read beamspot
  BeamSpot beamSpot;
  Handle<BeamSpot> beamSpotHandle;
  event.getByLabel("offlineBeamSpot", beamSpotHandle);
  beamSpot = *beamSpotHandle;
  const reco::BeamSpot &beamspot = *beamSpotHandle.product();

  std::vector<int> goodmuons;
  std::vector<int> goodphotons;

  {
    int counter = 0;
    for( MuonCollection::const_iterator  m = muons->begin(); m != muons->end(); ++m, ++counter){
      if (!(m->isGlobalMuon())) continue;
      if (!(m->globalTrack()->normalizedChi2()<10)) continue;
      if (!(m->globalTrack()->hitPattern().numberOfValidMuonHits()>0)) continue;
      if (!(m->isTrackerMuon())) continue;
      if (!(m->numberOfMatches()>1)) continue;
      if (!(m->track()->numberOfValidHits()>10)) continue;
      if (!(m->track()->hitPattern().numberOfValidPixelHits()>0)) continue;
      if (!(m->isolationR03().sumPt<3)) continue;
      if (!(m->pt()>10)) continue;
      if (!(fabs(m->eta())<2.4)) continue;
      if (fabs(m->globalTrack()->dxy(beamspot))>0.2) continue;
      goodmuons.push_back( counter );
    }
  }

  //    std::cout << "nr good muons " << goodmuons.size() << std::endl;

  {
    int counter = 0;
    for ( PhotonCollection::const_iterator  p = photons->begin(); p != photons->end(); ++p, ++counter){
      reco::SuperClusterRef scref = p->superCluster();
      float eta = fabs(scref->eta());
      if (eta>2.5) continue;
      if (1.4442<eta && eta<1.566) continue;
      if (!(p->pt()>10)) continue;
      DetId seed = scref->seed()->seed();
      EcalRecHitCollection::const_iterator theSeedHit = (seed.subdetId()==EcalBarrel) ? ebRecHits->find(seed) : eeRecHits->find(seed);
      int recoFlag = theSeedHit->recoFlag();
      int severityFlag = (seed.subdetId()==EcalBarrel) ? sevLv->severityLevel( seed.rawId(), *ebRecHits) : sevLv->severityLevel( seed.rawId(), *eeRecHits);
      if (recoFlag==2) continue;
      if (severityFlag==4 || severityFlag==5) continue;
      goodphotons.push_back( counter );
    }
  }

  //    std::cout << "nr good photons " << goodphotons.size() << std::endl;

  bool printout = false;
  //  if (goodmuons.size()>=2 && goodphotons.size()>=1) printout=true;

  bool globalpass = false;

  {
    bool found_already = false;
    for (std::vector<int>::const_iterator k1 = goodmuons.begin(); k1 != goodmuons.end(); ++k1){
      for (std::vector<int>::const_iterator k2 = goodmuons.begin(); k2 != goodmuons.end(); ++k2){
	
	if (k1>=k2) continue;
	const Muon* m1 = &(muons->at(*k1));
	const Muon* m2 = &(muons->at(*k2));
	if (printout) std::cout << "considering muons " << *k1 << " and " << *k2 << std::endl;

	if (m1->charge()+m2->charge()!=0) continue;

	if (printout) 	cout<<"passed charge"<<endl;

	TLorentzVector vec1(m1->px(),m1->py(),m1->pz(),m1->energy());
	TLorentzVector vec2(m2->px(),m2->py(),m2->pz(),m2->energy());
	float mass2body = (vec1+vec2).M();
	//	vec1.Print(); vec2.Print();
	//	cout << "mass2body " << mass2body << endl;
	if (mass2body<40 || mass2body>80) continue;
	
	if (printout) 	cout<<"passed mass"<<endl;

	for (std::vector<int>::const_iterator  k3 = goodphotons.begin(); k3 != goodphotons.end(); ++k3){
	  
	  const Photon* p = &(photons->at(*k3));
	  if (printout) 	  cout<<"consider photon " << *k3 <<endl;

	  TLorentzVector vec3(p->px(),p->py(),p->pz(),p->energy());
	  float mass3body = (vec1+vec2+vec3).M();
	  if (mass3body<70 || mass3body>110) continue;

	  if (printout) 	  cout <<"pass mass3 cut"<<endl;

	  float dr1 = reco::deltaR(m1->eta(),m1->phi(),p->eta(),p->phi());
	  float dr2 = reco::deltaR(m2->eta(),m2->phi(),p->eta(),p->phi());

	  if (dr1<0.8 || dr2<0.8) continue;

	  if (dr1<dr2){
	    if (m1->isolationR03().hadEt>1) continue;
	    if (m2->isolationR03().emEt>1) continue;
	  }
	  else {
	    if (m2->isolationR03().hadEt>1) continue;
	    if (m1->isolationR03().emEt>1) continue;
	  }

	  if (printout) 	  cout << "pass selection"<<endl;

	  if (found_already){
	    cout << "found new triple " << *k1 << " " << *k2 << " " << *k3 <<endl;
	    cout<<"CLEARING"<<endl;
	    outColMuon->clear();
	    outColPhoton->clear();
	    globalpass=false;
	    break;
	  }
	  outColMuon->push_back(muons->at(*k1));
	  outColMuon->push_back(muons->at(*k2));
	  outColPhoton->push_back(photons->at(*k3));
	  found_already=true;
	  globalpass=true;
	  //	  if (printout) {
	  //	  cout<<"pushed back triple " << *k1 << " " << *k2 << " " << *k3 <<endl;
	  //	  vec1.Print(); vec2.Print(); vec3.Print();
	  //	  std::cout << "Masses " << mass2body << " " << mass3body << std::endl;
	  //	  }

	}
      }
    }
  }


  event.put(outColMuon,"ZuugSelMuons");
  event.put(outColPhoton,"ZuugSelPhotons");

  //  if (globalpass) cout << "Found Zuug event " << event.id().run() << ":" << event.luminosityBlock() << ":" << event.id().event() << endl;
  //  std::cout << globalpass << std::endl;
  return globalpass;

}




// ------ method called once each job just before starting event loop  ---



void ZuugSelFilter::beginJob() {}



void ZuugSelFilter::endJob() {}



//define this as a plug-in
DEFINE_FWK_MODULE( ZuugSelFilter );

