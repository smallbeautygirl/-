
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Vector;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.table.AbstractTableModel;
import javax.swing.*;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.*;
import javax.swing.*;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class client {
  private Socket clientSocket;
  private DataInputStream dataInputStream;
  private DataOutputStream dataOutputStream;

  public static void main(String[] args) {
    try {
      client cli = new client();
    } catch (Exception e) {
      System.out.println(e);
    }
  }

  public client() throws UnknownHostException, IOException {
    Scanner keyboard = new Scanner(System.in);
    String address = null;
    int port = 0;

    System.out.println("Input your address");
    address = keyboard.next();
    System.out.println("Input your port");
    port = keyboard.nextInt();
    System.out.println("connection....");

    // 建立連線
    this.clientSocket = new Socket(address, port);
    System.out.println("Connection");
    this.getStreams();
    Frame mainframe = new Frame();
  }

  public Socket getSocket() {
    return this.clientSocket;
  }

  public void getStreams() throws IOException {
    this.dataInputStream = new DataInputStream(this.clientSocket.getInputStream());
    this.dataOutputStream = new DataOutputStream(this.clientSocket.getOutputStream());
  }

  public void sendData(String message) throws IOException {
    this.dataOutputStream.writeUTF(message);
  }

  class waitingroom extends JFrame {
    private JLabel waitingroomLabel = new JLabel("Welcom to waiting room!!");
    private JTable waitTable;
    private JLabel colAccount = new JLabel("Name");
    private JLabel colWin = new JLabel("Number of wins");
    private JLabel colLose = new JLabel("Number of loses");
    private Vector rowData = new Vector<String>();
    private Vector colData = new Vector<String>();

    public waitingroom() throws NumberFormatException, IOException {
      super("Waiting room");
      setSize(1200, 800);
      setLocationRelativeTo(null); // -->設定開啟的位置和某個物件相同，帶入null則會在畫面中間開啟
      setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);// DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
      setVisible(true);

      // 收幾個人wait和他們的資訊
      int countwait = 0;
      ArrayList waitInformation = new ArrayList<String>();
      String waitAccount = null;
      String waitWin = null;
      String waitLose = null;
      countwait = Integer.valueOf(dataInputStream.readUTF());
      for (int i = 0; i < countwait; ++i) {
        waitAccount = dataInputStream.readUTF();
        waitWin = dataInputStream.readUTF();
        waitLose = dataInputStream.readUTF();
        waitInformation.add(waitAccount);
        waitInformation.add(waitWin);
        waitInformation.add(waitLose);
      }

      // 建立Jtable
      this.colData.add("Name");
      this.colData.add("Number of win");
      this.colData.add("Number of lose");
      for(int i=0;i<countwait;++i){
        this.rowData.add(waitInformation.get(i));
        this.rowData.add(waitInformation.get(i+1));
        this.rowData.add(waitInformation.get(i+2));
      }
      this.waitTable = new JTable(rowData, colData);// 建立一个具有countwait+1列，3行的空表格
      this.waitTable.setFont(new Font("Arial",0,25));
      //this.waitTable.setBounds(250,200);
      // 容器
      Container waitroomContainer = getContentPane();
      waitroomContainer.setLayout(null);

      // 設定title lable
      this.waitingroomLabel.setFont(new Font("Arial", 1, 50));
      this.waitingroomLabel.setBounds(220, 100, 1000, 80);

      // 設定label
      this.colAccount.setFont(new Font("Arial", 0, 35));
      this.colWin.setFont(new Font("Arial", 0, 35));
      this.colLose.setFont(new Font("Arial", 0, 35));
      this.colAccount.setBounds(175, 200, 300, 60);
      this.colWin.setBounds(375, 200, 300, 60);
      this.colLose.setBounds(725, 200, 300, 60);

      waitroomContainer.add(this.waitingroomLabel);
      // waitroomContainer.add(this.colAccount);
      // waitroomContainer.add(this.colWin);
      // waitroomContainer.add(this.colLose);
      waitroomContainer.add(this.waitTable);
    }
  }

  class signinFrame extends JFrame {
    private JLabel accountLable = new JLabel("Account");
    private JLabel passwordLable = new JLabel("Password");
    private JPasswordField jPasswordField = new JPasswordField(5);
    private JTextField jTextField = new JTextField();
    private JButton Jbtn_YES = new JButton("sign in");
    private JButton Jbtn_NO = new JButton("cancel");

    public signinFrame() {
      super("Sign in");
      setSize(600, 400);
      setLocationRelativeTo(null); // -->設定開啟的位置和某個物件相同，帶入null則會在畫面中間開啟
      setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);// DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
      setVisible(true);
      Container container = getContentPane();
      container.setLayout(null);

      // 設定lable
      this.accountLable.setBounds(160, 50, 100, 40);
      this.accountLable.setFont(new Font("Arial", 0, 20));
      this.passwordLable.setBounds(160, 100, 100, 40);
      this.passwordLable.setFont(new Font("Arial", 0, 20));

      // 設定jTextField帳號輸入框大小位置及顯示字型
      this.jTextField.setBounds(280, 50, 180, 40);
      // 設定jPasswordField密碼輸入框大小位置及顯示字型
      this.jPasswordField.setBounds(280, 100, 180, 40);
      this.jPasswordField.setEchoChar('*');
      this.jPasswordField.setToolTipText("密碼長度5個字元");

      this.Jbtn_YES.setBounds(180, 250, 100, 40);
      this.Jbtn_YES.setFont(new Font("Arial", 0, 20));
      this.Jbtn_NO.setFont(new Font("Arial", 0, 20));
      this.Jbtn_NO.setBounds(330, 250, 100, 40);

      // 若按下signinButton 確認此帳戶存在則登入，若輸入錯誤則彈出警告視窗
      this.Jbtn_YES.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          try {
            String account = jTextField.getText();
            String password = String.copyValueOf(jPasswordField.getPassword());
            // 傳帳戶資料給server驗證
            sendData(account);
            sendData(password);

            String AccountIsExist = null;
            AccountIsExist = dataInputStream.readUTF();
            if (AccountIsExist.equals("true")) {
              waitingroom wr = new waitingroom();// 進入waiting room
            } else {
              JOptionPane.showMessageDialog(null, "Your account is not exist\nPlease create account first!!");
            }
            // System.out.println("account: " + account + " password: " + password);

            dispose();
            setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);// DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
          } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
          }
        }
      });
      this.Jbtn_NO.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {

          dispose();
        }
      });
      container.add(this.accountLable);
      container.add(this.passwordLable);
      container.add(this.jTextField);
      container.add(this.jPasswordField);
      container.add(this.Jbtn_YES);
      container.add(this.Jbtn_NO);
    }
  }

  class createAccountFrame extends JFrame {
    private JLabel accountLable = new JLabel("Account");
    private JLabel passwordLable = new JLabel("Password");
    private JPasswordField jPasswordField = new JPasswordField(5);
    private JTextField jTextField = new JTextField();
    private JButton Jbtn_YES = new JButton("create");
    private JButton Jbtn_NO = new JButton("cancel");

    public createAccountFrame() throws IOException {
      super("Create Account");
      setSize(600, 400);
      setLocationRelativeTo(null); // -->設定開啟的位置和某個物件相同，帶入null則會在畫面中間開啟
      setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);// DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
      setVisible(true);
      Container container = getContentPane();
      container.setLayout(null);

      // 設定lable
      this.accountLable.setBounds(160, 50, 100, 40);
      this.accountLable.setFont(new Font("Arial", 0, 20));
      this.passwordLable.setBounds(160, 100, 100, 40);
      this.passwordLable.setFont(new Font("Arial", 0, 20));

      // 設定jTextField帳號輸入框大小位置及顯示字型
      this.jTextField.setBounds(280, 50, 180, 40);
      // 設定jPasswordField密碼輸入框大小位置及顯示字型
      this.jPasswordField.setBounds(280, 100, 180, 40);
      this.jPasswordField.setEchoChar('*');
      this.jPasswordField.setToolTipText("密碼長度5個字元");

      this.Jbtn_YES.setBounds(180, 250, 100, 40);
      this.Jbtn_YES.setFont(new Font("Arial", 0, 20));
      this.Jbtn_NO.setFont(new Font("Arial", 0, 20));
      this.Jbtn_NO.setBounds(330, 250, 100, 40);

      // 若按下createAccountButton 則新增帳戶，若要創見的帳戶存在就請他直接登入
      this.Jbtn_YES.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          try {
            String account = jTextField.getText();
            String password = String.copyValueOf(jPasswordField.getPassword());
            sendData(account);
            sendData(password);
            System.out.println("account:" + account + " password:" + password);
            String AccountIsExist = null;
            AccountIsExist = dataInputStream.readUTF();
            System.out.println(AccountIsExist);
            if (AccountIsExist.equals("true")) {
              JOptionPane.showMessageDialog(null, "Your account is already exist\nPlease sign in!!");
            } else {
              waitingroom wr = new waitingroom();// 進入waiting room
            }
            // System.out.println("account: " + account + " password: " + password);
            dispose();
            setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);// DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
          } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
          }
        }
      });
      this.Jbtn_NO.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          dispose();
        }
      });
      container.add(this.accountLable);
      container.add(this.passwordLable);
      container.add(this.jTextField);
      container.add(this.jPasswordField);
      container.add(this.Jbtn_YES);
      container.add(this.Jbtn_NO);
    }
  }

  class Frame extends JFrame {
    public Font titlefont;
    public Font contentfont;

    public Frame() {
      super("Tic-Tac-Toe");
      setSize(1200, 800);
      setLocationRelativeTo(null); // -->設定開啟的位置和某個物件相同，帶入null則會在畫面中間開啟
      // 容器
      Container pn = getContentPane();

      pn.setLayout(null);

      // 設定字型
      this.titlefont = new Font("Arial", 1, 50);
      this.contentfont = new Font("Arial", 0, 30);

      // 設定title lable
      JLabel titleLabel = new JLabel("Tic-Tac-Toe");
      titleLabel.setFont(this.titlefont);
      titleLabel.setBounds(400, 200, 400, 50);

      // 設定snoopy lable
      ImageIcon snoopy = new ImageIcon("2.jpg");
      JLabel snoopyLabel = new JLabel(snoopy);
      snoopyLabel.setBounds(825, 390, 370, 370);

      // 設定按鈕
      JButton createAccountButton = new JButton("Create account");
      JButton signinButton = new JButton("Sign in");
      JButton exitButton = new JButton("Exit");
      signinButton.setFont(this.contentfont);
      createAccountButton.setFont(this.contentfont);
      exitButton.setFont(this.contentfont);
      signinButton.setBounds(415, 300, 280, 40);
      createAccountButton.setBounds(415, 400, 280, 40);
      exitButton.setBounds(415, 500, 280, 40);
      // 若按Exit 則關掉
      exitButton.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          try {
            sendData("exit");
          } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
          }
          // dispose();
          System.exit(0);
        }
      });
      // 若按下createAccountButton 則新增帳戶
      createAccountButton.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          try {
            sendData("create");
            createAccountFrame caf = new createAccountFrame();
          } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
          }
        }
      });

      // 若按下signinButton 則新增帳戶
      signinButton.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
          try {
            sendData("sign in");
            signinFrame sf = new signinFrame();
          } catch (IOException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
          }
        }
      });
      pn.add(createAccountButton);
      pn.add(signinButton);
      pn.add(exitButton);
      pn.add(titleLabel);
      pn.add(snoopyLabel);
      // 關閉選項(右上角的叉叉圖示)按下後的動作
      // EXIT_ON_CLOSE：點選關閉時，關閉程式
      // DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
      // HIDE_ON_CLOSE：點選關閉時，僅隱藏顯示的視窗，程式仍在背景執行
      setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      setVisible(true);
      setContentPane(pn);
    }
  }

  class ClientInformation {
    private String account = null;
    private String password = null;

    public ClientInformation(String account, String password) {
      this.account = account;
      this.password = password;
    }
  }

}