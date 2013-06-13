import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000


##                      _              _       
##   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___ 
##  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
## | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
##  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
##                                              
################################################


isMC = False

if isMC:
    InputFileName = "Photon_tagProbeTree_Zee_mc.root"
    OutputFilePrefix = "efficiency-mc-"
else:
    InputFileName = "Photon_tagProbeTree_Zee_data.root"
    OutputFilePrefix = "efficiency-data-"



################################################
PDFName = "pdfSignalPlusBackground"
if isMC:
    PDFName = ""
################################################


EfficiencyBins = cms.PSet(
#    probe_pt = cms.vdouble( 25,30,35,40,50,80,200 ),
#    probe_eta = cms.vdouble( -2.5,-2.1,-1.8,-1.566,-1.4442,-1.2,-0.9,-0.5,0,0.5,0.9,1.2,1.4442,1.566,1.8,2.1,2.5 )
    probe_pt = cms.vdouble( 25,200 ),
    probe_eta = cms.vdouble( 0,1.4442 ) 
)

EfficiencyBinningSpecification = cms.PSet(
    #specifies what unbinned variables to include in the dataset, the mass is needed for the fit
    UnbinnedVariables = cms.vstring("mass"),
    #specifies the binning of parameters
    BinnedVariables = cms.PSet(EfficiencyBins),
    #first string is the default followed by binRegExp - PDFname pairs
    BinToPDFmap = cms.vstring(PDFName)
)

#### For MC truth: do truth matching
EfficiencyBinningSpecificationMC = cms.PSet(
    UnbinnedVariables = cms.vstring("mass"),
    BinnedVariables = cms.PSet(
#    probe_pt = cms.vdouble( 25,30,35,40,50,80,200 ),
#    probe_eta = cms.vdouble( -2.5,-2.1,-1.8,-1.566,-1.4442,-1.2,-0.9,-0.5,0,0.5,0.9,1.2,1.4442,1.566,1.8,2.1,2.5 ),
    probe_pt = cms.vdouble( 25,200 ),
    probe_eta = cms.vdouble( -2.5,-1.4442,1.4442,2.5 ),
    mcTrue = cms.vstring("true")
    ),
    BinToPDFmap = cms.vstring()  
)



##########################################################################################
############################################################################################
if isMC:
    mcTruthModules = cms.PSet(
        MCtruth_passingPhotonID = cms.PSet(
        EfficiencyBinningSpecificationMC,
        EfficiencyCategoryAndState = cms.vstring("probe_passingPhotonID","pass")
        )
        )
else:
    mcTruthModules = cms.PSet()
##########################################################################################
##########################################################################################

Categories_MC = cms.PSet(
    weight = cms.vstring("weight", "0.0", "10.0", ""),
    mcTrue = cms.vstring("MC true", "dummy[true=1,false=0]"),
    probe_passingPhotonID = cms.vstring("probe_passingPhotonID", "dummy[pass=1,fail=0]")
    )
Categories_data = cms.PSet(
    probe_passingPhotonID = cms.vstring("probe_passingPhotonID", "dummy[pass=1,fail=0]")
    )
    
if isMC:
    Categories_touse=Categories_MC
else:
    Categories_touse=Categories_data


process.PhotonToIsoId = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(80),
    Quiet = cms.untracked.bool(False),
    # IO parameters:
    InputFileNames = cms.vstring(InputFileName),
    InputDirectoryName = cms.string("PhotonToIsoId"),
    InputTreeName = cms.string("fitter_tree"),
    OutputFileName = cms.string(OutputFilePrefix+"PhotonToIsoId.root"),
    #numbrer of CPUs to use for fitting
    NumCPU = cms.uint32(1),
    # specifies wether to save the RooWorkspace containing the data for each bin and
    # the pdf object with the initial and final state snapshots
    SaveWorkspace = cms.bool(True),
    floatShapeParameters = cms.bool(True),
    #fixVars = cms.vstring("mean"),                                                 
    # defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
    Variables = cms.PSet(
        mass = cms.vstring("Tag-Probe Mass", "70.0", "110.0", "GeV/c^{2}"),
        probe_pt = cms.vstring("Probe p_{T}", "0", "100", "GeV/c"),
        probe_eta = cms.vstring("Probe #eta", "-2.5", "2.5", ""),                
    ),
    # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
    Categories=Categories_touse,
    # defines all the PDFs that will be available for the efficiency calculations; uses RooFit's "factory" syntax;
    # each pdf needs to define "signal", "backgroundPass", "backgroundFail" pdfs, "efficiency[0.9,0,1]" and "signalFractionInPassing[0.9]" are used for initial values  
    PDFs = cms.PSet(
    pdfSignalPlusBackground = cms.vstring(
    ##     "CBExGaussShape::signalRes(mass, mean[2.0946e-01], sigma[8.5695e-04],alpha[3.8296e-04], n[6.7489e+00], sigma_2[2.5849e+00], frac[6.5704e-01])",  ### the signal function goes here
#    "CBExGaussShape::signalResPass(mass, meanP[0.], sigmaP[8.5695e-04, 0., 3.],alphaP[3.8296e-04], nP[6.7489e+00], sigmaP_2[2.5849e+00], fracP[6.5704e-01])",  ### signal resolution for "pass" sample
#    "CBExGaussShape::signalResFail(mass, meanF[2.0946e-01, -5., 5.], sigmaF[8.5695e-04, 0., 5.],alphaF[3.8296e-04], nF[6.7489e+00], sigmaF_2[2.5849e+00], fracF[6.5704e-01])",  ### signal resolution for "fail" sample     
#    "ZGeneratorLineShape::signalPhy(mass)", ### NLO line shape
#    "RooCMSShape::backgroundPass(mass, alphaPass[60.,50.,70.], betaPass[0.001, 0.,0.1], betaPass, peakPass[90.0])",
#    "RooCMSShape::backgroundFail(mass, alphaFail[60.,50.,70.], betaFail[0.001, 0.,0.1], betaFail, peakFail[90.0])",
#    "FCONV::signalPass(mass, signalPhy, signalResPass)",
#    "FCONV::signalFail(mass, signalPhy, signalResFail)",     

    "MyTemplateShape::signalPhyP(mass, probe_pt, probe_eta, blabla1[1.0])",
#    "MyTemplateShape::signalPhyF(mass, probe_pt, probe_eta, blabla2[0.0])",

    "RooCBShape::signalResPass(mass, meanP[0.,-2.,2.], sigmaP[0.5, 0.0, 5.0], alphaP[2.0, 0.1, 25.0], nP[10.0, 1.0, 50.0])",
#    "RooCBShape::signalResFail(mass, meanF[0.,-2.,2.], sigmaF[0.5, 0.0, 5.0], alphaF[2.0, 0.1, 25.0], nF[10.0, 1.0, 50.0])",

    "RooExponential::signalF1(mass,cF1[-0.2,-2.,0])",
    "RooCBShape::signalF2(mass, meanF[90.,70.,110.], sigmaF[5.,2.,20.], alphaF[2.0, 0.1, 25.0], nF[10.0, 1.0, 50.0])",
    "SUM::signalFail(fF[0.5,0.,1.] * signalF1, signalF2)",

    "FCONV::signalPass(mass, signalPhyP, signalResPass)",
#    "FCONV::signalFail(mass, signalPhyF, signalResFail)",
    
    "RooCMSShape::backgroundPass(mass, alphaPass[50.], betaPass[1.0], gammaPass[0.03, 0.001, 0.1], peakPass[90.0])",
    "RooCMSShape::backgroundFail(mass, alphaFail[50.], betaFail[1.0], gammaFail[0.03, 0.001, 0.1], peakFail[90.0])",


    "efficiency[0.9,0,1]",
    "signalFractionInPassing[1.0]"     
    #"Gaussian::signal(mass, mean[91.2, 89.0, 93.0], sigma[2.3, 0.5, 10.0])",
    #"RooExponential::backgroundPass(mass, cPass[-0.02,-5,0])",
    #"RooExponential::backgroundFail(mass, cFail[-0.02,-5,0])",
    #"efficiency[0.9,0,1]",
    #"signalFractionInPassing[0.9]"
        ),
    
    
    ),

                                       # defines a set of efficiency calculations, what PDF to use for fitting and how to bin the data;
                                       # there will be a separate output directory for each calculation that includes a simultaneous fit, side band subtraction and counting. 
                                       Efficiencies = cms.PSet(
    mcTruthModules,
    passingPhotonID = cms.PSet(
    EfficiencyBinningSpecification,
    EfficiencyCategoryAndState = cms.vstring("probe_passingPhotonID","pass")
    )
    )
                                       )

if isMC:
    process.PhotonToIsoId.WeightVariable = cms.string("PUweight")



process.fit = cms.Path(
    process.PhotonToIsoId
    )
