//
//  ViewController.swift
//  shift
//
//  Created by scott on 11/06/2020.
//  Copyright © 2020 scott. All rights reserved.
//

import Foundation
import UIKit

class MainViewController: UIViewController {
    struct Holiday: Decodable {
        var hid: Int
        var description: String
        var month: String
        var day: String
        var year: String
    }
        
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    func createDynamicObjects(data: [Holiday]) {
        // because there are only two buttons preloaded
        if self.view.subviews.count > 2 {
            self.view.subviews[2].removeFromSuperview()
            self.view.subviews[2].removeFromSuperview()
        }
          
        var yPos = 90
        
        for i in 0...1 {
            let label = UILabel()

            let value1 = String(data[i].hid)
            let value2 = data[i].description + " " + data[i].month

            let value = "value 1: " + value1 + " value 2: " + value2

            label.text = value
            label.textAlignment = .center
            label.frame = CGRect(x:10, y:yPos, width:294, height: 80)
            yPos += 85
                        
            self.view.addSubview(label)
        }
    }
    
    @IBAction func BtnGetData(_ sender: Any) {
        let url = NSURL(string: "http://localhost/shift/api/search/")
         
        var request = URLRequest(url: url! as URL)
        request.httpMethod = "POST"

        let dataString = "month=06&day=21"
        let dataD = dataString.data(using: .utf8) // convert to utf8 string

        do
        {
            // the upload task, uploadJob, is defined here
            let uploadJob = URLSession.shared.uploadTask(with: request, from: dataD)
            {
                data, response, error in
                
                if error != nil {
                    // display an alert if there is an error inside the DispatchQueue.main.async
                    DispatchQueue.main.async
                    {
                        let alert = UIAlertController(title: "Message", message: "Please, verify your internet connection.", preferredStyle: .alert)
                        alert.addAction(UIAlertAction(title: "Accept", style: .cancel, handler: nil))
                        self.present(alert, animated: true, completion: nil)
                    }
                }
                else
                {
                    if let unwrappedData = data {
                        // Response from web server hosting the database
                        let returnedData = NSString(data: unwrappedData, encoding: String.Encoding.utf8.rawValue)
                        
                        let model = try! JSONDecoder().decode([Holiday]?.self, from: unwrappedData) as [Holiday]?
                        
                        DispatchQueue.main.async
                        {
                            self.createDynamicObjects(data: model!)
                        }
                                                
                        if returnedData != "" // response data
                        {
                            // display an alert if no error and database
                            // insert worked (return = 1) inside the DispatchQueue.main.async
                            DispatchQueue.main.async
                            {
                                let alert = UIAlertController(title: "Message", message: "The API calling was successfully.", preferredStyle: .alert)
                                alert.addAction(UIAlertAction(title: "Accept", style: .cancel, handler: nil))
                                self.present(alert, animated: true, completion: nil)
                            }
                        }
                        else
                        {
                            // display an alert if an error and database
                            // insert didn't worked (return != 1) inside the DispatchQueue.main.async
                            DispatchQueue.main.async
                            {
                                let alert = UIAlertController(title: "Message", message: "The API calling didn't work successfully.", preferredStyle: .alert)
                                alert.addAction(UIAlertAction(title: "Accept", style: .cancel, handler: nil))
                                self.present(alert, animated: true, completion: nil)
                            }
                        }
                    }
                }
            }
            
            uploadJob.resume()
        }
        
    }
        
    @IBAction func BtnMoveNextScreen(_ sender: Any) {
        let next = self.storyboard?.instantiateViewController(withIdentifier: "ConfirmController") as! ConfirmViewController
        self.navigationController?.pushViewController(next, animated: true)
    }
}
