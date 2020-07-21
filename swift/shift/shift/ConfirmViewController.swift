//
//  ConfirmViewController.swift
//  shift
//
//  Created by scott on 13/06/2020.
//  Copyright © 2020 scott. All rights reserved.
//

import UIKit

class ConfirmViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func BtnMoveNextScreen(_ sender: Any) {
        let next = self.storyboard?.instantiateViewController(withIdentifier: "SignUpController") as! SignUpViewController
        self.navigationController?.pushViewController(next, animated: true)
    }
        
    @IBAction func BtnMovePreviousScreen(_ sender: Any) {
        let previous = self.navigationController?.viewControllers[0] as! MainViewController
        self.navigationController?.popToViewController(previous, animated: true)
    }
    
    @IBAction func BtnShowCamera(_ sender: Any) {
        let camera = self.storyboard?.instantiateViewController(withIdentifier: "CameraController") as! CameraViewController
        self.navigationController?.pushViewController(camera, animated: true)
    }
}
