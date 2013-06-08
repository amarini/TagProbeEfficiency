import FWCore.ParameterSet.Config as cms

#GLOBAL_TAG = "FT42_V24_AN1::All"
GLOBAL_TAG = 'START42_V14B::All'

##    ___            _           _      
##   |_ _|_ __   ___| |_   _  __| | ___ 
##    | || '_ \ / __| | | | |/ _` |/ _ \
##    | || | | | (__| | |_| | (_| |  __/
##   |___|_| |_|\___|_|\__,_|\__,_|\___|

process = cms.Process("Skimmer")
#stuff needed for prescales
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = GLOBAL_TAG
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
                                     SkipEvent = cms.untracked.vstring('ProductNotFound')
                                     )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000


##   ____             _ ____                           
##  |  _ \ ___   ___ | / ___|  ___  _   _ _ __ ___ ___ 
##  | |_) / _ \ / _ \| \___ \ / _ \| | | | '__/ __/ _ \
##  |  __/ (_) | (_) | |___) | (_) | |_| | | | (_|  __/
##  |_|   \___/ \___/|_|____/ \___/ \__,_|_|  \___\___|
##  

readFiles = cms.untracked.vstring()

process.source = cms.Source("PoolSource", 
                            fileNames = readFiles
                            )
readFiles.extend([
'/store/user/peruzzi/DYJetsToLL_Summer11_START42_V11_test.root'
#'/store/user/peruzzi/DYJetsToLL_53_newG4_START53_V7D_AODSIM_test.root'
    ])

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )    
process.source.inputCommands = cms.untracked.vstring("keep *","drop *_MEtoEDMConverter_*_*")

process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi")

process.ZuugSelection = cms.EDFilter("ZuugSelFilter",
                                       src_muons = cms.untracked.InputTag("muons"),
                                       src_photons = cms.untracked.InputTag("photons")
                                       )

process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                         applyfilter = cms.untracked.bool(True),
                                         debugOn = cms.untracked.bool(False),
                                         numtrack = cms.untracked.uint32(10),
                                         thresh = cms.untracked.double(0.25)
                                         )

process.goodVertices = cms.EDFilter("VertexSelector",
                                    src = cms.InputTag("offlinePrimaryVertices"),
                                    cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"),
                                    filter = cms.bool(True)
                                    )


### HLT filter
import copy
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
process.ZToMMGHltFilter = copy.deepcopy(hltHighLevel)
process.ZToMMGHltFilter.throw = cms.bool(False)
process.ZToMMGHltFilter.HLTPaths = ["*Mu*"]

process.ZToMMGMuonsCountFilter = cms.EDFilter("CandViewCountFilter",
                                          src = cms.InputTag("muons"),
                                          minNumber = cms.uint32(2)
                                          )

process.ZToMMGLooseMuons = cms.EDFilter("MuonViewRefSelector",
                                src = cms.InputTag("muons"),
                                cut = cms.string("""
                                pt > 10 &
                                isGlobalMuon &
                                isTrackerMuon &
                                abs(innerTrack().dxy) < 2.0
                                """),
                                filter = cms.bool(True)
                                )

process.ZToMMGLooseMuonsCountFilter = cms.EDFilter("CandViewCountFilter",
                                           src = cms.InputTag("ZToMMGLooseMuons"),
                                           minNumber = cms.uint32(2)
                                           )

process.ZToMMGTightMuons = process.ZToMMGLooseMuons.clone(
    src = "ZToMMGLooseMuons",
    cut = "pt > 20"
    )

process.ZToMMGDimuons = cms.EDProducer("CandViewShallowClonePtrCombiner",
                               decay = cms.string("ZToMMGTightMuons ZToMMGLooseMuons"),
                               checkCharge = cms.bool(False),
                               cut = cms.string("30 < mass")
                               )

process.ZToMMGDimuonsFilter = cms.EDFilter("CandViewCountFilter",
                                   src = cms.InputTag("ZToMMGDimuons"),
                                   minNumber = cms.uint32(1)
                                   )

process.ZToMMGSkimFilterSequence = cms.Sequence(
#    process.ZToMMGHltFilter +
    process.ZToMMGMuonsCountFilter +
    (process.ZToMMGLooseMuons + process.ZToMMGLooseMuonsCountFilter) *
    process.ZToMMGTightMuons *
    process.ZToMMGDimuons *
    process.ZToMMGDimuonsFilter
    )

process.skimmer = cms.Path(
    process.scrapingVeto*process.goodVertices*process.ZToMMGSkimFilterSequence*process.ZuugSelection
    )

process.Out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string ("SkimZuugEventFile.root"),
                               SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('skimmer')
    ),
                               outputCommands = cms.untracked.vstring(
    'keep *',
    'drop *_*_*_Skimmer' 
    )
                               )
process.outpath = cms.EndPath(process.Out)
