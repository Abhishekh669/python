


// fn main() {
//     // println!("Hello, world!");

//     // variable in the rust ;
//     // variable in the rust are ummutable so if we code as below it shows the error 
//     // let x = 5;
//     // println!("The value of x is {}", x);
//     // x = 1;
//     // println!("The new value of the x is {}",x);
    
//     // in this way we can change the variable value 
//     // let mut x = 5;
//     // println!("The value of the x is {}",x);
//     // x=6 ;
//     // println!("The new value of the x is {}",x);


//     let x = 6;
//     let x = x+1; 
//     println!("{}",x);

//     let word = "Hello";
//     println!("this length of the variable word is {}",word.len());
//     hell("abhishekh".to_string());

//     // now for the loops 
//     println!("Using the loop for looping it is like while(true)");
//     looping_with_loop();
//     println!("Using the while for looping it is like while(true)");
//     looping_with_while();
//     println!("Using the for [1] for looping it is like while(true)");
//     looping_with_for1();
//     println!("Using the for [2] for looping it is like while(true)");
//     looping_with_for2()
    
    

    

// }

// fn looping_with_for1(){
//     let a = [1, 2, 4, 5, 6, 7, 20];
//     for element in a.iter(){
//         println!("I am {}", element);
//     }
//     println!(
//         "Finished looping with for 1 "
//     )
// }

// fn looping_with_for2(){
//     for i in 1..10{
//         println!(" This is  : {}",i)
//     }
//     println!("Completed looping with for 2")
// }


// fn hell(name : String) -> u16{
//     println!("My name is {}", name );
//     6
// }


// fn looping_with_loop(){
//     let mut x = 0;
//     loop{
//         x = x + 1;
//         println!(" {} : i am being looped", x);
//         if x == 4{
//             break;
//         }
        
//     }
// }

// fn looping_with_while(){
//     let mut num = 4;
//     while num != 0{
//         println!(" i am now {}",num);
//         num -= 1;
//     }
//     println!("Completed Looping of while ")
// }



fn main(){
    let given_string = "AabB8COPQpqr98".to_string();
    
    
    
    let small_alpha = small_character();
    let capital_alpha = capital_character();
    println!("Small:  {:?}", small_alpha);  // `{:?}` is used for debug printing of Vec
    println!("Capital: {:?}", capital_alpha);
    let   step_one_text = decode_rot13(given_string);
    println!("{}", step_one_text)
   

}




fn decode_rot13(word : String) -> String{
    let mut new_decoded_word= String::new();
    for i in word.chars(){
        if i.is_ascii_alphabetic(){
            if i.is_uppercase(){
                // let i_asci = char::from_u32(i as u32).unwrap()
                let i_asci = i as u8;
                let add_13 = i_asci + 13 ;
                if add_13  > 90 {
                    let new_value = ((add_13 - 65)-26)+65;
                    let new_character = char::from_u32(new_value as u32).unwrap();
                    new_decoded_word.push(new_character);
                } else{
                    let hello_world = char::from_u32(add_13 as u32).unwrap();
                    new_decoded_word.push(hello_world);
                }
                println!("decoded is : {}",new_decoded_word)
            }
            else {
                let i_asci = i as u8;
                let add_13 = i_asci + 13;
                if add_13 > 122{
                    let new_value = ((add_13 - 97) -26) + 97;
                    let new_character = char::from_u32(new_value as u32).unwrap();
                    new_decoded_word.push(new_character);
                }else{
                    let hello_world = char::from_u32(add_13 as u32).unwrap();
                    new_decoded_word.push(hello_world);
                }
            }
        } 
        else{
            new_decoded_word.push(i);
        }  
    }
    new_decoded_word.to_string()

        
}


fn small_character() ->Vec<char>{
    let mut vec  =  vec![];
    for i in 97..=(97+25){
        let  character= char::from_u32(i as u32).unwrap();
        vec.push(character);
    }
    vec

}


fn capital_character() ->Vec<char>{
    let mut vec = vec![];
    for  i  in 65..=(65+25){
        let  character = char::from_u32(i as u32).unwrap();
        vec.push(character)
    }
    vec

    

}