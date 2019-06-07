import java.io.*;
import java.net.*;
import java.awt.*;
import java.util.*;
import javax.swing.*;
import java.awt.event.*;
import javax.swing.event.*;
import javax.imageio.ImageIO;

public class Client {
	private static String host	= "127.0.0.1";
    private static int port	= 8888;

    private static Socket socket				= null;
    private static ObjectInputStream input		= null;
    private static ObjectOutputStream output	= null;

    private static JFrame frame		= null;
    private static JPanel MainPanel	= null;

    private static String name			= null;

    public static void main(String[] argv) {
    	SwingUtilities.invokeLater(new Runnable(){
            @Override
            public void run() {
                Client client = new Client();
            }
        });
    }

	public Client() {

		/* --------------------------- prepare GUI --------------------------- */

		this.frame = new JFrame("Tic-Tac-Toe");
		this.frame.setSize(800, 600);
		this.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		JPanel page1 = new Page1();
		JPanel page2 = new Page2();
		JPanel page3 = new Page3();

		this.MainPanel = new Panel();
		this.MainPanel.add(page1, "page1");
		this.MainPanel.add(page2, "page2");
		this.MainPanel.add(page3, "page3");

		frame.getContentPane().add(MainPanel);
		frame.setVisible(true);

		/* ------------------------ Connect to Server ------------------------ */

		Thread connectThread = new Thread(Connection);
		connectThread.start();
    }

    private Runnable Connection = new Runnable() {
        @Override
        public void run() {
			try {
				Client.socket	= new Socket(Client.host, Client.port);
				Client.output	= new ObjectOutputStream(Client.socket.getOutputStream());
				Client.input	= new ObjectInputStream(Client.socket.getInputStream());
            } catch (IOException e) {
				JOptionPane.showMessageDialog(Client.frame, "Can't connect to Server!", "Network Error", JOptionPane.ERROR_MESSAGE);
				System.exit(0);
            } finally {
            	System.out.println("Connect Successfully");
            }
        }
    };

    class mGridBagConstraints extends GridBagConstraints {
    	mGridBagConstraints(int fill, int anchor, int gridx, int gridy, Insets insets, double weightx, double weighty) {
    		super();
    		this.fill		= fill;
    		this.gridx		= gridx;
    		this.gridy		= gridy;
    		this.insets		= insets;
			this.weightx	= weightx;
			this.weighty	= weighty;
    	}
    }

    class Panel extends JPanel {
		Panel() {
			super();
			this.setLayout(new CardLayout());
			this.setBackground(Color.WHITE);
		}
    }

    class Page extends JPanel {
		Page() {
			super(new GridBagLayout());
    		this.setBackground(Color.WHITE);
    	}
    }

     class Page1 extends Page {
		Page1() {
			super();

    		JLabel titleLabel	= new JLabel("Tic-Tac-Toe", JLabel.CENTER);
			JLabel userLabel	= new JLabel("User Name: ", JLabel.CENTER);
			JTextField userText	= new JTextField();
			JButton startButton	= new btn_primary("Start");

			titleLabel.setFont(new Font("Monospac", Font.BOLD, 36));
			userLabel.setFont(new Font("Monospac", Font.PLAIN, 18));

			this.add(titleLabel, new mGridBagConstraints(GridBagConstraints.HORIZONTAL, GridBagConstraints.CENTER, 0, 0, new Insets(0, 0, 50, 0), 0, 0));
			this.add(userLabel, new mGridBagConstraints(GridBagConstraints.NONE, GridBagConstraints.WEST, 0, 1, new Insets(0, -130, 15, 0), 0, 0));
			this.add(userText, new mGridBagConstraints(GridBagConstraints.BOTH, GridBagConstraints.WEST, 1, 1, new Insets(0, -110, 15, -40), 0, 0));
			this.add(startButton, new mGridBagConstraints(GridBagConstraints.NONE, GridBagConstraints.CENTER, 0, 2, new Insets(0, 0, 0, 0), 0, 0));

			startButton.addActionListener(new ActionListener() {
				@Override
				public void actionPerformed(ActionEvent ae) {
					if(userText.getText().isEmpty())
						JOptionPane.showMessageDialog(Client.frame, "Pleas input user name!");
					else {
						Client.name				= userText.getText();
						CardLayout cardLayout	= (CardLayout)Client.MainPanel.getLayout();
						cardLayout.show(Client.MainPanel, "page2");

						try {
							Client.output.writeObject(Client.name);
						} catch(IOException e) {
							e.printStackTrace();
						}
					}
				}
			});
    	}
    }

    class Page2 extends Page implements Runnable {
		private JPanel playerPanel;
		private Thread thread;

		Page2() {
			super();
			this.playerPanel	= new Page();
			JLabel titleLabel	= new JLabel("Waiting room", JLabel.CENTER);

			titleLabel.setFont(new Font("Monospac", Font.BOLD, 36));

			this.add(titleLabel, new mGridBagConstraints(GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTH, 0, 0, new Insets(0, 0, 10, 0), 1.0, 0));
			this.add(this.playerPanel, new mGridBagConstraints(GridBagConstraints.BOTH, GridBagConstraints.NORTH, 0, 1, new Insets(0, 0, 400, 0), 1.0, 1.0));

			this.thread = new Thread(this);
    		this.thread.start();
    	}

    	@Override
		public void run() {
			try {
				while(true) {
					if(Client.input == null) continue;
					
					int request = (int)Client.input.readObject();
					
					if(request == 1) {
						CardLayout cardLayout = (CardLayout)Client.MainPanel.getLayout();
						cardLayout.show(Client.MainPanel, "page3");
					}
					
					Vector<Info> list = (Vector<Info>)Client.input.readObject();
					this.playerPanel.removeAll();

					for(int i = 0; i < list.size(); i++) {
						if(list.get(i).name.equals(Client.name)) continue;
						
						final int index			= i;
						JPanel player			= new Page();
						JLabel playerLabel		= new JLabel(list.get(i).name, JLabel.CENTER);
						JLabel stateLabel		= new JLabel(list.get(i).state, JLabel.CENTER);
						JButton inviteButton	= new btn_primary("Invite");

						playerLabel.setFont(new Font("Monospac", Font.PLAIN, 18));
						stateLabel.setFont(new Font("Monospac", Font.PLAIN, 18));

						player.add(playerLabel, new mGridBagConstraints(GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTH, 0, 0, new Insets(0, 0, 10, 0), 0.6, 0));
						player.add(stateLabel, new mGridBagConstraints(GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTH, 1, 0, new Insets(0, 0, 10, 0), 0.6, 0));
						player.add(inviteButton, new mGridBagConstraints(GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTH, 2, 0, new Insets(0, 50, 10, 50), 0, 0));
						player.setBorder(BorderFactory.createMatteBorder(0, 0, 1, 0, Color.black));
						
						this.playerPanel.add(player, new mGridBagConstraints(GridBagConstraints.HORIZONTAL, GridBagConstraints.NORTH, 0, i, new Insets(0, 0, 0, 0), 1.0, 0));
						
						inviteButton.addActionListener(new ActionListener() {
							@Override
							public void actionPerformed(ActionEvent ae) {
								if(!list.get(index).state.equals("IDLE")) 
									JOptionPane.showMessageDialog(Client.frame, list.get(index).name + " is unaviable.");
								else {
									try {
										int request = 1;
										Client.output.writeObject(request);
										Client.output.writeObject(list.get(index).name);
									} catch(IOException e) {
										e.printStackTrace();
									}
									
									CardLayout cardLayout = (CardLayout)Client.MainPanel.getLayout();
									cardLayout.show(Client.MainPanel, "page3");
								}
							}
						});
					}

					this.playerPanel.revalidate();
					this.playerPanel.repaint();
				}
			} catch(IOException | ClassNotFoundException e) {
				e.printStackTrace();
			}
		}
    }

    class Page3 extends Page {
		private JPanel mainPanel;
		private JButton[] cellButtons;
		
		Page3() {
			super();
			
			this.mainPanel		= new Page();
			this.cellButtons	= new btn[9];
			
			for(int i = 0; i < 9; i++) {
				JPanel cellPanel	= new Page();
				this.cellButtons[i]	= new btn();
				this.cellButtons[i].setMinimumSize(new Dimension(266, 200));
				this.cellButtons[i].setMaximumSize(new Dimension(266, 200));
				this.cellButtons[i].setPreferredSize(new Dimension(266, 200));
				this.cellButtons[i].setFont(new Font("Monospac", Font.PLAIN, 128));
				
				cellPanel.add(this.cellButtons[i], new mGridBagConstraints(GridBagConstraints.BOTH, GridBagConstraints.CENTER, 0, 0, new Insets(0, 0, 0, 0), 1.0, 1.0));
				mainPanel.add(cellPanel, new mGridBagConstraints(GridBagConstraints.BOTH, GridBagConstraints.CENTER, i / 3, i % 3, new Insets(0, 0, 0, 0), 1.0, 1.0));
				cellPanel.setBorder(BorderFactory.createMatteBorder(1, 1, 1, 1, Color.black));
				
				this.cellButtons[i].addActionListener(new ActionListener() {
					@Override
					public void actionPerformed(ActionEvent ae) {
						try {
							JButton button = (JButton) ae.getSource();
							if(button.getText().equals(""))
								button.setText("O");
						} catch(Exception e) {
							e.printStackTrace();
						}
					}
				});				
			}
			
			this.add(mainPanel, new mGridBagConstraints(GridBagConstraints.BOTH, GridBagConstraints.CENTER, 0, 0, new Insets(0, 0, 0, 0), 1.0, 1.0));
    	}
    }

	class btn extends JButton {

        private Color hoverBackgroundColor;
        private Color pressedBackgroundColor;
		
		public btn() {
            this("");
        }

        public btn(String text) {
            super(text);

            this.setFont(new Font("Monospac", Font.PLAIN, 18));
            super.setContentAreaFilled(false);
			this.setFocusPainted(false);
			
			this.setForeground(new Color(33, 37, 41));
			this.setBackground(new Color(248, 249, 250));
			this.setHoverBackgroundColor(new Color(226, 230, 234));
			this.setPressedBackgroundColor(new Color(218, 224, 229));
        }

        @Override
        protected void paintComponent(Graphics g) {
            if (getModel().isPressed()) {
                g.setColor(pressedBackgroundColor);
            }
            else if (getModel().isRollover()) {
                g.setColor(hoverBackgroundColor);
            }
            else {
                g.setColor(getBackground());
            }
            g.fillRect(0, 0, getWidth(), getHeight());
            super.paintComponent(g);
        }

        @Override
        public void setContentAreaFilled(boolean b) { }

        public void setHoverBackgroundColor(Color hoverBackgroundColor) {
            this.hoverBackgroundColor = hoverBackgroundColor;
        }

        public void setPressedBackgroundColor(Color pressedBackgroundColor) {
            this.pressedBackgroundColor = pressedBackgroundColor;
        }
    }

	class btn_primary extends btn {
		public btn_primary(String text) {
			super(text);
			this.setForeground(Color.WHITE);
			this.setBackground(new Color(0, 123, 255));
			this.setHoverBackgroundColor(new Color(0, 105, 217));
			this.setPressedBackgroundColor(new Color(0, 98, 204));
		}
	}
}
