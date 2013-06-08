#ifndef PhysicsTools_TagAndProbe_ZuugSelFilter_h
#define PhysicsTools_TagAndProbe_ZuugSelFilter_h

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"


// forward declarations

class ZuugSelFilter : public edm::EDFilter 
{
 public:
  explicit ZuugSelFilter(const edm::ParameterSet&);
  ~ZuugSelFilter();

 private:
  virtual void beginJob() ;
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
      
  // ----------member data ---------------------------

  edm::InputTag src_muons_;
  edm::InputTag src_photons_;

};

#endif
