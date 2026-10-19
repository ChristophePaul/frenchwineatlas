import Foundation
import Vision
import AppKit
// usage: ocr <image> ...  -> prints recognised text lines per image (top-to-bottom)
for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["fr-FR"]
    req.usesLanguageCorrection = true
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let obs = (req.results ?? []).sorted { $0.boundingBox.minY > $1.boundingBox.minY }
    print("=== " + (path as NSString).lastPathComponent)
    for o in obs { if let t = o.topCandidates(1).first { print(t.string) } }
}
