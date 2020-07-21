//
//  SignUp.swift
//  shift
//
//  Created by scott on 13/06/2020.
//  Copyright © 2020 scott. All rights reserved.
//

import UIKit

class SignUpViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func BtnMovePreviousScreen(_ sender: Any) {
        let previous = self.storyboard?.instantiateViewController(withIdentifier: "ConfirmController") as! ConfirmViewController
        self.navigationController?.pushViewController(previous, animated: true)
    }
        
    @IBAction func BtnMoveInitialScreen(_ sender: Any) {
        self.navigationController?.popToRootViewController(animated: true)
    }    
}
