import FWCore.ParameterSet.Config as cms

##                      _              _       
##   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___ 
##  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
## | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
##  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
##                                              
########################

MC_flag = False
#MC_flag = True

FirstRunForPVDistro = False


if MC_flag:
    GLOBAL_TAG = 'START42_V14B::All'
else:
    GLOBAL_TAG = "FT42_V24_AN1::All"


OUTPUT_FILE_NAME = "Photon_tagProbeTree.root"
RECOProcess = "RECO"

##    ___            _           _      
##   |_ _|_ __   ___| |_   _  __| | ___ 
##    | || '_ \ / __| | | | |/ _` |/ _ \
##    | || | | | (__| | |_| | (_| |  __/
##   |___|_| |_|\___|_|\__,_|\__,_|\___|

process = cms.Process("TagProbe")
#stuff needed for prescales
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = GLOBAL_TAG
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
##process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
##                                     SkipEvent = cms.untracked.vstring('ProductNotFound')
##                                     )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

############ Needed for pileup re-weighting ########## SHOULD CONTAIN THE DISTRIBUTION OF NPV AS PRODUCED BY THIS WORKFLOW
process.pileupReweightingProducer = cms.EDProducer("PileupWeightProducer",
                                                   PileupMCFile = cms.untracked.string("pileup_Zee_mc.root"),
                                                   PileupDataFile = cms.untracked.string("pileup_Zee_data.root")
                                                   )

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


if MC_flag:
    readFiles.extend([
        '/store/user/peruzzi/event_files_for_testing/DYJetsToLL_test.root'
        ])
else:
    readFiles.extend([
        '/store/user/peruzzi/Zuug_skim_2011_unpublishable/DoubleMu-Run2011A-16Jan2012-v1/SkimZuugEventFile_10_2_UeA.root'
        ])
    

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )    
process.source.inputCommands = cms.untracked.vstring("keep *","drop *_MEtoEDMConverter_*_*")


process.dump=cms.EDAnalyzer('EventContentAnalyzer')

### HLT filter
import copy
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
process.ZTnPHltFilter = copy.deepcopy(hltHighLevel)
process.ZTnPHltFilter.throw = cms.bool(False)
process.ZTnPHltFilter.HLTPaths = ["HLT_Ele32_CaloIdL_CaloIsoVL_SC17*","HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17*"]


ELECTRON_ET_CUT_MIN = 32.0
ELECTRON_COLL = "gsfElectrons"
ELECTRON_CUTS = "ecalDrivenSeed==1 && (abs(superCluster.eta)<2.5) && !(1.4442<abs(superCluster.eta)<1.566) && (ecalEnergy*sin(superClusterPosition.theta)>" + str(ELECTRON_ET_CUT_MIN) + ")"
####

PHOTON_COLL = "photons"
PHOTON_CUTS = "hadronicOverEm<0.15 && (abs(superCluster.eta)<2.5) && !(1.4442<abs(superCluster.eta)<1.566) && (superCluster.energy*sin(superCluster.position.theta)>20)"
####


process.goodPhotons = cms.EDFilter(
    "PhotonSelector",
    src = cms.InputTag( PHOTON_COLL ),
    cut = cms.string(PHOTON_CUTS)
    )


process.electronHLTMatching = cms.EDProducer("ElectronHLTMatching",
                                             InputCollection = cms.InputTag(ELECTRON_COLL),
                                             TriggerResults = cms.InputTag("TriggerResults", "", "HLT"),
                                             HLTTriggerSummaryAOD = cms.InputTag("hltTriggerSummaryAOD", "", "HLT"),
                                             TriggerPaths = cms.vstring("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17","HLT_Ele32_CaloIdL_CaloIsoVL_SC17"),
                                             ModuleLabels = cms.vstring("hltEle32CaloIdTCaloIsoTTrkIdTTrkIsoTSC17TrackIsolFilter","hltEle32CaloIdLCaloIsoVLSC17TrackIsolFilter"),
                                             RecoCuts = cms.string(""),
                                             HLTCuts = cms.string(""),
                                             DeltaR = cms.double(0.2),
                                             DoMatching = cms.bool(True)
                                             )


#process.electronHLTMatching = cms.EDProducer("trgMatchedGsfElectronProducer",
#                                             InputProducer = cms.InputTag( ELECTRON_COLL ),
#                                             hltTags = cms.VInputTag(cms.InputTag("HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17","", "HLT"),cms.InputTag("HLT_Ele32_CaloIdL_CaloIsoVL_SC17","", "HLT")),
#                                             triggerEventTag = cms.untracked.InputTag("hltTriggerSummaryAOD","","HLT"),
#                                             triggerResultsTag = cms.untracked.InputTag("TriggerResults","","HLT")
#                                             )

#  GsfElectron ################
process.elePassingWP80 = cms.EDFilter("GsfElectronRefSelector",
                                      src = cms.InputTag( "electronHLTMatching" ),
                                      cut = cms.string(
    str(ELECTRON_CUTS) +
    " && (gsfTrack.trackerExpectedHitsInner.numberOfHits==0 && !(-0.02<convDist<0.02 && -0.02<convDcot<0.02))"
    " && ((isEB"
    " && ( dr03TkSumPt/p4.Pt <0.09 && dr03EcalRecHitSumEt/p4.Pt < 0.07 && dr03HcalTowerSumEt/p4.Pt  < 0.1 )"
    " && (sigmaIetaIeta<0.01)"
    " && ( -0.06<deltaPhiSuperClusterTrackAtVtx<0.06 )"
    " && ( -0.004<deltaEtaSuperClusterTrackAtVtx<0.004 )"
    " && (hadronicOverEm<0.04)"
    ")"
    " || (isEE"
    " && ( dr03TkSumPt/p4.Pt <0.04 && dr03EcalRecHitSumEt/p4.Pt < 0.05 && dr03HcalTowerSumEt/p4.Pt  < 0.025 )"
    " && (sigmaIetaIeta<0.03)"
    " && ( -0.03<deltaPhiSuperClusterTrackAtVtx<0.03 )"
    " && ( -0.007<deltaEtaSuperClusterTrackAtVtx<0.007 )"
    " && (hadronicOverEm<0.025) "
    "))"
    )
                                      )
#if MC_flag:
#    process.elePassingWP80.src = cms.InputTag( ELECTRON_COLL )





##     ___           _       _   _             
##    |_ _|___  ___ | | __ _| |_(_) ___  _ __  
##     | |/ __|/ _ \| |/ _` | __| |/ _ \| '_ \ 
##     | |\__ \ (_) | | (_| | |_| | (_) | | | |
##    |___|___/\___/|_|\__,_|\__|_|\___/|_| |_|

                                         
#  Isolation ################
#ECAL and HCAL only
if MC_flag==True:
    process.photonID = cms.EDFilter("PhotonRefSelector",
                                    src = cms.InputTag("goodPhotons"),
                                    cut = cms.string(
        "((r9>0.9) || (ecalRecHitSumEtConeDR03 < (0.012*pt + 4)))"
        "&& ((r9>0.9) || (hcalTowerSumEtConeDR03 < (0.005*pt + 4 )))"
        "&& ((r9>0.9) || (trkSumPtHollowConeDR03 < (0.002*pt + 4)))"
        "&& ((r9<0.9) || (ecalRecHitSumEtConeDR03 < (0.012*pt + 50)))"
        "&& ((r9<0.9) || (hcalTowerSumEtConeDR03 < (0.005*pt + 50 )))"
        "&& ((r9<0.9) || (trkSumPtHollowConeDR03 < (0.002*pt + 50)))"
        " && (hcalTowerSumEtConeDR03 < (0.005*pt + 4 ))"
        " && (trkSumPtHollowConeDR03 < (0.002*pt + 4))"
        " && (hadronicOverEm<0.05)"
        " && (abs(superCluster.eta)>1.4442 || 0.87*sigmaIetaIeta+0.0011<0.011) && (abs(superCluster.eta)<1.566 || 0.99*sigmaIetaIeta<0.030)"
        )
                                    )
else:
    process.photonID = cms.EDFilter("PhotonRefSelector",
                                    src = cms.InputTag("goodPhotons"),
                                    cut = cms.string(
        "((r9>0.9) || (ecalRecHitSumEtConeDR03 < (0.012*pt + 4)))"
        "&& ((r9>0.9) || (hcalTowerSumEtConeDR03 < (0.005*pt + 4 )))"
        "&& ((r9>0.9) || (trkSumPtHollowConeDR03 < (0.002*pt + 4)))"
        "&& ((r9<0.9) || (ecalRecHitSumEtConeDR03 < (0.012*pt + 50)))"
        "&& ((r9<0.9) || (hcalTowerSumEtConeDR03 < (0.005*pt + 50 )))"
        "&& ((r9<0.9) || (trkSumPtHollowConeDR03 < (0.002*pt + 50)))"
        " && (hadronicOverEm<0.05)"
        " && (abs(superCluster.eta)>1.4442 || sigmaIetaIeta<0.011) && (abs(superCluster.eta)<1.566 || sigmaIetaIeta<0.030)"
        )
                                    )




##    _____             ____        __ _       _ _   _             
##   |_   _|_ _  __ _  |  _ \  ___ / _(_)_ __ (_) |_(_) ___  _ __  
##     | |/ _` |/ _` | | | | |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \ 
##     | | (_| | (_| | | |_| |  __/  _| | | | | | |_| | (_) | | | |
##     |_|\__,_|\__, | |____/ \___|_| |_|_| |_|_|\__|_|\___/|_| |_|
##              |___/                                              

process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi")

process.photon_sequence = cms.Sequence(
    process.goodPhotons +
    process.elePassingWP80 +
    process.photonID
    )


##    _____ ___   ____    ____       _          
##   |_   _( _ ) |  _ \  |  _ \ __ _(_)_ __ ___ 
##     | | / _ \/\ |_) | | |_) / _` | | '__/ __|
##     | || (_>  <  __/  |  __/ (_| | | |  \__ \
##     |_| \___/\/_|     |_|   \__,_|_|_|  |___/
##                                              
##   
#  Tag & probe selection ######
process.tagPhoton = cms.EDProducer("CandViewShallowCloneCombiner",
                                   decay = cms.string("elePassingWP80 goodPhotons"),
                                   checkCharge = cms.bool(False),
                                   cut = cms.string("60 < mass < 120")
                                   )
process.tagphotonID = process.tagPhoton.clone()
process.tagphotonID.decay = cms.string("elePassingWP80 photonID")

process.allTagsAndProbes = cms.Sequence(
    process.tagPhoton +
    process.tagphotonID
)


##    __  __  ____   __  __       _       _               
##   |  \/  |/ ___| |  \/  | __ _| |_ ___| |__   ___  ___ 
##   | |\/| | |     | |\/| |/ _` | __/ __| '_ \ / _ \/ __|
##   | |  | | |___  | |  | | (_| | || (__| | | |  __/\__ \
##   |_|  |_|\____| |_|  |_|\__,_|\__\___|_| |_|\___||___/
##                                                        

process.McMatchEle = cms.EDProducer("MCTruthDeltaRMatcherNew",
                                    matchPDGId = cms.vint32(11),
                                    src = cms.InputTag("elePassingWP80"),
                                    distMin = cms.double(0.3),
                                    matched = cms.InputTag("genParticles"),
                                    checkCharge = cms.bool(True)
                                    )
process.McMatchPhoton = process.McMatchEle.clone()
process.McMatchPhoton.matchPDGId = cms.vint32(11)
process.McMatchPhoton.src = cms.InputTag("goodPhotons")
process.McMatchPhoton.checkCharge = cms.bool(False)
process.McMatchPhotonID = process.McMatchEle.clone()
process.McMatchPhotonID.matchPDGId = cms.vint32(11)
process.McMatchPhotonID.src = cms.InputTag("photonID")
process.McMatchPhotonID.checkCharge = cms.bool(False)

process.mc_sequence = cms.Sequence(
   process.McMatchEle +
   process.McMatchPhoton +
   process.McMatchPhotonID 
)

############################################################################
##    _____           _       _ ____            _            _   _  ____  ##
##   |_   _|_ _  __ _( )_ __ ( )  _ \ _ __ ___ | |__   ___  | \ | |/ ___| ##
##     | |/ _` |/ _` |/| '_ \|/| |_) | '__/ _ \| '_ \ / _ \ |  \| | |  _  ##
##     | | (_| | (_| | | | | | |  __/| | | (_) | |_) |  __/ | |\  | |_| | ##
##     |_|\__,_|\__, | |_| |_| |_|   |_|  \___/|_.__/ \___| |_| \_|\____| ##
##              |___/                                                     ##
##                                                                        ##
############################################################################
##    ____                      _     _           
##   |  _ \ ___ _   _ ___  __ _| |__ | | ___  ___ 
##   | |_) / _ \ | | / __|/ _` | '_ \| |/ _ \/ __|
##   |  _ <  __/ |_| \__ \ (_| | |_) | |  __/\__ \
##   |_| \_\___|\__,_|___/\__,_|_.__/|_|\___||___/


## I define some common variables for re-use later.
## This will save us repeating the same code for each efficiency category

ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    pt  = cms.string("pt"),
    phi  = cms.string("phi"),
#    et  = cms.string("et"),
#    e  = cms.string("energy"),
#    p  = cms.string("p"),
#    px  = cms.string("px"),
#    py  = cms.string("py"),
#    pz  = cms.string("pz"),
#    theta  = cms.string("theta"),    
#    vx     = cms.string("vx"),
#    vy     = cms.string("vy"),
#    vz     = cms.string("vz"),
#    rapidity  = cms.string("rapidity"),
    mass  = cms.string("mass"),
#    mt  = cms.string("mt"),    
)   


TagVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    pt  = cms.string("pt"),
    phi  = cms.string("phi"),
#    mass  = cms.string("mass"),
#    px  = cms.string("px"),
#    py  = cms.string("py"),
#    pz  = cms.string("pz"),
#    ## super cluster quantities
#    sc_energy = cms.string("superCluster.energy"),
#    sc_et     = cms.string("superCluster.energy*sin(superCluster.position.theta)"),    
#    sc_eta    = cms.string("superCluster.eta"),
#    sc_phi    = cms.string("superCluster.phi"),
)


ProbePhotonVariablesToStore = cms.PSet(
        probe_eta = cms.string("eta"),
        probe_phi  = cms.string("phi"),
        probe_pt  = cms.string("pt"),
#        probe_px  = cms.string("px"),
#        probe_py  = cms.string("py"),
#        probe_pz  = cms.string("pz"),
        ## isolation 
        probe_trkSumPtHollowConeDR03 = cms.string("trkSumPtHollowConeDR03"),
        probe_ecalRecHitSumEtConeDR03  = cms.string("ecalRecHitSumEtConeDR03"),
        probe_hcalTowerSumEtConeDR03  = cms.string("hcalTowerSumEtConeDR03"),
#        probe_trkSumPtHollowConeDR04 = cms.string("trkSumPtHollowConeDR04"),
#        probe_ecalRecHitSumEtConeDR04  = cms.string("ecalRecHitSumEtConeDR04"),
#        probe_hcalTowerSumEtConeDR04  = cms.string("hcalTowerSumEtConeDR04"),
        ## booleans
#        probe_isPhoton  = cms.string("isPhoton"),     
        ## Hcal energy over Ecal Energy
        probe_hadronicOverEm = cms.string("hadronicOverEm"),
        ## Cluster shape information
        probe_sigmaIetaIeta_NOTSCALED = cms.string("sigmaIetaIeta"),
        ## Pixel seed
        probe_hasPixelSeed = cms.string("hasPixelSeed"),
        probe_sc_energy = cms.string("superCluster.energy"),
        probe_sc_et     = cms.string("superCluster.energy*sin(superCluster.position.theta)"),    
        probe_sc_eta    = cms.string("superCluster.eta"),
        probe_sc_phi    = cms.string("superCluster.phi")
)


CommonStuffForPhotonProbe = cms.PSet(
   variables = cms.PSet(ProbePhotonVariablesToStore),
   ignoreExceptions =  cms.bool (False),
   #fillTagTree      =  cms.bool (True),
   addRunLumiInfo   =  cms.bool (True),
   addEventVariablesInfo   =  cms.bool (True),
   pairVariables =  cms.PSet(ZVariablesToStore),
   pairFlags     =  cms.PSet(
#          mass60to120 = cms.string("60 < mass < 120")
    ),
    tagVariables   =  cms.PSet(TagVariablesToStore),
    tagFlags     =  cms.PSet(
#          flag = cms.string("pt>0")
    ),    
)



if MC_flag:
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(MC_flag),
        tagMatches = cms.InputTag("McMatchEle"),
        motherPdgId = cms.vint32(23), 
        makeMCUnbiasTree = cms.bool(MC_flag),
        checkMotherInUnbiasEff = cms.bool(MC_flag),
        mcVariables = cms.PSet(
        probe_eta = cms.string("eta"),
        probe_pt  = cms.string("pt"),
        probe_phi  = cms.string("phi"),
#        probe_mass  = cms.string("mass"),
#        probe_et  = cms.string("et"),
#        probe_e  = cms.string("energy"),
#        probe_p  = cms.string("p"),
#        probe_px  = cms.string("px"),
#        probe_py  = cms.string("py"),
#        probe_pz  = cms.string("pz"),
#        probe_theta  = cms.string("theta"),    
#        probe_vx     = cms.string("vx"),
#        probe_vy     = cms.string("vy"),
#        probe_vz     = cms.string("vz"),   
#        probe_charge = cms.string("charge"),
#        probe_rapidity  = cms.string("rapidity"),    
#        probe_mass  = cms.string("mass"),
#        probe_mt  = cms.string("mt")
        ),
        mcFlags     =  cms.PSet(
#        probe_flag = cms.string("pt>0")
        ),      
        )
else:
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )


##    ___                 ___    _ 
##  |_ _|___  ___       |_ _|__| |
##   | |/ __|/ _ \       | |/ _` |
##   | |\__ \ (_) |  _   | | (_| |
##   |___|___/\___/  ( ) |___\__,_|
##                   |/            
##  Photon --> isolation, id  etc.

process.PhotonToIsoId = cms.EDAnalyzer("TagProbeFitTreeProducer",
    ## pick the defaults
    mcTruthCommonStuff,
    CommonStuffForPhotonProbe,
    # choice of tag and probe pairs, and arbitration                 
    tagProbePairs = cms.InputTag("tagPhoton"),
    arbitration   = cms.string("None"),                      
    flags = cms.PSet(
        probe_passingPhotonID = cms.InputTag("photonID")
    ),
    probeMatches  = cms.InputTag("McMatchPhoton"),
    allProbes     = cms.InputTag("goodPhotons")
)
if MC_flag:
    if FirstRunForPVDistro==False:
        process.PhotonToIsoId.PUWeightSrc = cms.InputTag("pileupReweightingProducer","pileupWeights")


process.tree_sequence = cms.Sequence(
    process.PhotonToIsoId
    )    

##    ____       _   _     
##   |  _ \ __ _| |_| |__  
##   | |_) / _` | __| '_ \ 
##   |  __/ (_| | |_| | | |
##   |_|   \__,_|\__|_| |_|
##

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticles"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(True),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( 1,2,3 )
                                   )


#process.path = cms.Path(process.printTree)

if MC_flag:
    process.tagAndProbe = cms.Path(
        process.ZTnPHltFilter *
        (
        process.electronHLTMatching +
        process.photon_sequence +
        process.allTagsAndProbes + process.pileupReweightingProducer +
        process.mc_sequence + 
        process.tree_sequence
        )
        )
else:
    process.tagAndProbe = cms.Path(
        process.ZTnPHltFilter *
        (
        process.electronHLTMatching +
        process.photon_sequence +
        process.allTagsAndProbes +
        process.tree_sequence
        )
        )

if MC_flag:
    if FirstRunForPVDistro:
        process.tagAndProbe.remove(process.pileupReweightingProducer)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(OUTPUT_FILE_NAME)
                                   )
