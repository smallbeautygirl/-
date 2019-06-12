
import java.util.ArrayList;
import java.util.Formatter;
import java.util.Scanner;
import java.util.Vector;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import javax.swing.table.AbstractTableModel;
import javax.swing.*;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
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
  private ArrayList waitInformation = new ArrayList<>();
  private String myName = "";

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

  class recevewait extends Thread {
    private Container container;
    private JLabel waitingroomLabel = new JLabel("Welcom to waiting room!!");
    private JTable waitTable;
    private JLabel colAccount = new JLabel("Name");
    private JLabel colWin = new JLabel("Number of wins");
    private JLabel colLose = new JLabel("Number of loses");
    private Vector rowData = new Vector<String>();
    private Vector colData = new Vector<String>();
    private JButton start = new JButton("start");
  
    private int count =0;
    public recevewait(Container container) {
      this.count=0;
      this.container = container;
      System.out.println("recevewait");
      // 設定jbutton
      this.start.addActionListener(new ActionListener() {
        //private int flag;

        public void actionPerformed(ActionEvent e) {
          if (waitInformation.size() >= 6) {// 若waiting room裡有兩人以上，就可以開始玩
            try {
              sendData(myName);// 傳自己是誰
              System.out.println(myName);
              sendData("start");// 告訴server 我開始了
              System.out.println("start");
            } catch (IOException e1) {
              // TODO Auto-generated catch block
              e1.printStackTrace();
            }
            TicTacToe tic = new TicTacToe();
          } else {
            JOptionPane.showMessageDialog(null, "Please wait other player!!");
          }
        }
      });
    }

    public void run() {
      int tag = 0;
      while (true) {
        try {
          String data = dataInputStream.readUTF();
          System.out.println(data);
          if(data.equals("end")){
            System.out.println("end wait thread");
              return;
          }
          this.container.removeAll();
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

          this.start.setFont(new Font("Arial", 0, 35));
          this.start.setBounds(500, 650, 200, 60);

          this.container.add(this.waitingroomLabel);
          this.container.add(this.colAccount);
          this.container.add(this.colWin);
          this.container.add(this.colLose);
          this.container.add(this.start);

          boolean IsExist = false;

          if (data.length() >= 3) {
            for (int i = 0; i < waitInformation.size(); i += 3) {
              if (waitInformation.get(i).equals(data)) {// 如果account已經存在就不用加進去arraylist了
                IsExist = true;
                tag = 0;
                break;
              }
            }
            if (!IsExist) {
              tag = 1;// name不存在arraylist裡
            }
          }
          if (tag == 1) {
            waitInformation.add(data);
          }

          JLabel[] lable = new JLabel[waitInformation.size()];
          System.out.println(waitInformation.size());
          int distance = 0;
          for (int i = 0; i < waitInformation.size(); ++i) {
            lable[i] = new JLabel(waitInformation.get(i).toString());
            lable[i].setFont(new Font("Arial", 0, 35));
            if (i % 3 == 0) {
              lable[i].setBounds(175, 250 + distance, 300, 60);
            } else if (i % 3 == 2) {
              lable[i].setBounds(375, 250 + distance, 300, 60);
              distance += 50;
            } else {
              lable[i].setBounds(725, 250 + distance, 300, 60);
            }
            container.add(lable[i]);
          }

          this.container.revalidate();
          this.container.repaint();

        } catch (Exception e) {
          e.printStackTrace();
        }
      }
    }
  }

  class TicTacToe extends JFrame implements Runnable {
    private JTextField idField;// textfield to display player's mark
    private JTextArea displayArea;// JTextArea to display output
    private JPanel boardPanel;// panel for tic-tac-toe board
    private JPanel panel2;// panel to hold board
    private Square[][] board;// tic-tac-toe board
    private Square currentSquare;// current square
    private Scanner input;// input from server
    private Formatter output;// output to server
    private final String X_MARK = "X";// mark for first client
    private final String O_MARK = "O";// mark for second client
    private boolean myTurn;
    private String myMark;

    // set up tic-tac-toe server and GUI that displays messages
    public TicTacToe(){
      super(myName);
      this.displayArea = new JTextArea(4, 30);// set up JTextArea
      this.displayArea.setEditable(false);
      add(new JScrollPane(this.displayArea), BorderLayout.SOUTH);

      this.boardPanel = new JPanel();// set up panel for square in board
      this.boardPanel.setLayout(new GridLayout(3, 3, 0, 0));

      board = new Square[3][3];// create square

      for (int row = 0; row < board.length; row++) {
        for (int column = 0; column < board[row].length; column++) {
          // create square
          board[row][column] = new Square(" ", row * 3 + column);
          boardPanel.add(board[row][column]);// add square
        }
      }

      idField = new JTextField();
      idField.setEditable(false);
      add(idField, BorderLayout.NORTH);

      panel2 = new JPanel();
      panel2.add(boardPanel, BorderLayout.CENTER);
      add(panel2, BorderLayout.CENTER);

      setSize(300, 225);
      this.setLocationRelativeTo(null); // -->設定開啟的位置和某個物件相同，帶入null則會在畫面中間開啟
      setVisible(true);
      startClient();
    }// end Tic constructor

    public void startClient() {
      System.out.println("startClient constructor");
      try {
        // get streams for intput and output
        input = new Scanner(clientSocket.getInputStream());
        output = new Formatter(clientSocket.getOutputStream());
      } catch (IOException ioException) {
        ioException.printStackTrace();
      }
      ExecutorService worker = Executors.newFixedThreadPool(1);
      worker.execute(this);
    }

    public void run() {
      System.out.println("play");
      myMark = input.nextLine();// get player's mark(O or X)
      System.out.println("Mymark is "+myMark);
      SwingUtilities.invokeLater(new Runnable() {
        public void run() {
          // display player's mark
          idField.setText("You are player \"" + myMark + "\"");
        }
      });

      myTurn = (myMark.equals(X_MARK));
      while (true) {
        if (input.hasNextLine()) {
          processMessage(input.nextLine());
        }
      }
    }

    // process message received by client
    private void processMessage(String message) {
      // valid move occured
      if (message.equals("Valid move")) {
        displayMessage("Valid move, please wait.\n");
        setMark(currentSquare, myMark);
      } else if (message.equals("InValid move, try again")) {
        displayMessage(message + "\n");// display invalid move
        myTurn = true;
      } else if (message.equals("Opponent moved")) {
        int location = input.nextInt();
        input.nextLine();
        int row = location / 3;
        int column = location % 3;

        setMark(board[row][column], (myMark.equals(X_MARK) ? O_MARK : X_MARK));
        displayMessage("Opponent moved. Your turn\n");
        myTurn = true;
      } else {
        displayMessage(message + "\n");
      }

    }

    private void displayMessage(final String messageToDisplay) {
      SwingUtilities.invokeLater(new Runnable() {
        public void run() {
          displayArea.append(messageToDisplay);// update output
        }
      });
    }

    private void setMark(final Square squareToMark, final String mark) {
      SwingUtilities.invokeLater(new Runnable() {
        public void run() {
          squareToMark.setMark(mark);// set mark in square
        }
      });
    }

    public void sendClickedSquare(int location) {
      if (myTurn) {
        output.format("%d\n", location);// send location to server
        output.flush();
        myTurn = false;
      }
    }

    public void setCurrentSquare(Square square) {
      this.currentSquare = square;
    }

    private class Square extends JPanel {
      private String mark;// mark to be drawn in this square
      private int location;// location of square

      public Square(String squareMark, int squareLocation) {
        this.mark = squareMark;
        this.location = squareLocation;

        addMouseListener(new MouseAdapter() {
          public void mouseReleased(MouseEvent e) {
            setCurrentSquare(Square.this);

            // send location of this square
            sendClickedSquare(getSquareLocation());
          }
        });
      }

      // return preferred size of square
      public Dimension getPreferredSize() {
        return new Dimension(30, 30);
      }

      // return minimum size of square
      public Dimension getMinimumSize() {
        return getPreferredSize();
      }

      // set mark for Square
      public void setMark(String newMark) {
        this.mark = newMark;
        repaint();// repaint square
      }

      // return square location
      public int getSquareLocation() {
        return this.location;
      }

      // draw Square
      public void paintComponent(Graphics g) {
        super.paintComponent(g);

        g.drawRect(0, 0, 29, 29);// draw square 29 29
        g.drawString(this.mark, 11, 20);// draw mark 11 20
      }
    }
  }

  class waitingroom extends JFrame {

    public waitingroom() throws NumberFormatException, IOException {
      super("Waiting room");
      this.setSize(1200, 800);
      this.setLocationRelativeTo(null); // -->設定開啟的位置和某個物件相同，帶入null則會在畫面中間開啟
      this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);// DISPOSE_ON_CLOSE：點選關閉時，關閉顯示的視窗以及使用的資源，程式仍在背景執行
      this.setVisible(true);

      // 容器
      Container waitroomContainer = getContentPane();
      waitroomContainer.setLayout(null);
      recevewait rewait = new recevewait(waitroomContainer);
      rewait.start();
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
              myName = account;
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
              myName = account;
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