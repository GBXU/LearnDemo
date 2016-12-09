package com.Servlet;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import java.util.Properties;

import javax.activation.DataHandler;
import javax.activation.DataSource;
import javax.activation.FileDataSource;
import javax.mail.Authenticator;
import javax.mail.BodyPart;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.NoSuchProviderException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

/**
 * Servlet implementation class SendEmail
 */
@WebServlet("/SendEmail")
public class SendEmail extends HttpServlet {
	private static final long serialVersionUID = 1L;
	
	// �ϴ��ļ��洢Ŀ¼
    private static final String UPLOAD_DIRECTORY = "upload";
    // �ϴ�����
    private static  int MEMORY_THRESHOLD   = 1024 * 1024 * 3;  // 3MB
    private static final int MAX_FILE_SIZE      = 1024 * 1024 * 40; // 40MB
    private static final int MAX_REQUEST_SIZE   = 1024 * 1024 * 50; // 50MB
    
    private String filePath;
    private String fileName;
    /**
     * @see HttpServlet#HttpServlet()
     */
    public SendEmail() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) 
			throws ServletException, IOException {
   }

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String from_passwd = null;
		/******************upload**********************/
		// ����Ƿ�Ϊ��ý���ϴ�
		if (!ServletFileUpload.isMultipartContent(request)) {
		    // ���������ֹͣ
		    PrintWriter writer = response.getWriter();
		    writer.println("Error: ��������� enctype=multipart/form-data");
			    writer.flush();
			    return;
		}
	    // �����ϴ�����
	    DiskFileItemFactory factory = new DiskFileItemFactory();
	    // �����ڴ��ٽ�ֵ - �����󽫲�����ʱ�ļ����洢����ʱĿ¼��
	    factory.setSizeThreshold(MEMORY_THRESHOLD);
	    // ������ʱ�洢Ŀ¼
	    factory.setRepository(new File(System.getProperty("java.io.tmpdir")));
	    ServletFileUpload upload = new ServletFileUpload(factory);     
	    // ��������ļ��ϴ�ֵ
	    upload.setFileSizeMax(MAX_FILE_SIZE);
	    // �����������ֵ (�����ļ��ͱ�����)
	    upload.setSizeMax(MAX_REQUEST_SIZE);
	    // ������ʱ·�����洢�ϴ����ļ�
	    // ���·����Ե�ǰӦ�õ�Ŀ¼
	    String uploadPath = getServletContext().getRealPath("./") + File.separator + UPLOAD_DIRECTORY;
	    // ���Ŀ¼�������򴴽�
        File uploadDir = new File(uploadPath);
        if (!uploadDir.exists()) {
            uploadDir.mkdir();
        }
        try {
        @SuppressWarnings("unchecked")// ���������������ȡ�ļ�����
            List<FileItem> formItems = upload.parseRequest(request);
            if (formItems != null && formItems.size() > 0) {
                // ����������
	            for (FileItem item : formItems) {
	                // �����ڱ��е��ֶ�
	                if (!item.isFormField()) {
	                    fileName = new File(item.getName()).getName();
	                    filePath = uploadPath + File.separator + fileName;
	                    File storeFile = new File(filePath);
	                    // �ڿ���̨����ļ����ϴ�·��
	                    System.out.println(filePath);
	                    // �����ļ���Ӳ��
	                    item.write(storeFile);
//	                    request.setAttribute("message",
//	                        "OK");
	                }else {
	                	//��Ϊenctype="multipart/form-data"�ѱ�ȫ��ת��Ϊ�ֽ���
	                	//����getParameter()�޷�����ʹ��
	                	if(item.getFieldName().compareTo("passwd")==0){
	                		from_passwd = item.getString();
	                	}
					}
	            }
            }
	    } catch (Exception ex) {
//	        request.setAttribute("message",
//	                "NULL");
	    }
	    // ��ת�� message.jsp
	    //getServletContext().getRequestDispatcher("/message.jsp").forward(request, response);
	    /******************email**********************/
		// �ռ��˵ĵ����ʼ� ID
		String to = "932739864@qq.com";
				//request.getParameter("email");
		// �����˵ĵ����ʼ� ID
		String from = "2014141462281@stu.scu.edu.cn";
		
		
		System.out.println(from_passwd);
		// �������Ǵӱ����������͵����ʼ�
		String host = "mail.scu.edu.cn";
		// ��ȡ����������
		Properties properties =new Properties();
		properties.setProperty("mail.debug", "true");// ����debug����
		properties.setProperty("mail.smtp.auth", "true");// ���ͷ�������Ҫ�����֤
		properties.setProperty("mail.host", host);// �����ʼ�������������
		properties.setProperty("mail.transport.protocol", "smtp");// �����ʼ�Э������
		// ��ȡĬ�ϵ� Session ����
		Session session = Session.getDefaultInstance(properties,new MyAuthenticator(from,from_passwd));

		// ������Ӧ��������
		response.setContentType("text/html;charset=UTF-8");
		PrintWriter out = response.getWriter();

		try{
			// ����һ��Ĭ�ϵ� MimeMessage ����
			MimeMessage message = new MimeMessage(session);
			// ���� From: header field of the header.
			message.setFrom(new InternetAddress(from));
			// ���� To: header field of the header.
			message.addRecipient(Message.RecipientType.TO, new InternetAddress(to));
			// ���� Subject: header field
			message.setSubject("This is the Subject Line!");
			// ������Ϣ���� 
			BodyPart messageBodyPart = new MimeBodyPart();
			// ��д��Ϣ
			messageBodyPart.setText("This is message body");
 
			// ����һ���ಿ����Ϣ
			Multipart multipart = new MimeMultipart();
 
			// �����ı���Ϣ����
			multipart.addBodyPart(messageBodyPart);
 
			// �ڶ������Ǹ���
			messageBodyPart = new MimeBodyPart();
			String filename = fileName;
			DataSource source = new FileDataSource(filePath);
			messageBodyPart.setDataHandler(new DataHandler(source));
			messageBodyPart.setFileName(filename);
			multipart.addBodyPart(messageBodyPart);
			
			// ������������Ϣ����
			message.setContent(multipart );
			
			// ������Ϣ
			Transport.send(message);
			String title = "���͵����ʼ�";
			String res = "�ɹ����͵����ʼ�...";
			String docType = "<!DOCTYPE html> \n";
			out.println(docType +
					"<html>\n" +
					"<head><title>" + title + "</title></head>\n" +
					"<body bgcolor=\"#f0f0f0\">\n" +
					"<h1 align=\"center\">" + title + "</h1>\n" +
					"<p align=\"center\">" + res + "</p>\n" +
					"</body></html>");
			}catch (MessagingException mex) {
				mex.printStackTrace();
			}
	}
	public class MyAuthenticator extends Authenticator{
		private String user;  
		private String pwd; 
		public MyAuthenticator(String user, String pwd) {
	        this.user = user;  
	        this.pwd = pwd;  
		}
	    @Override 
	    protected PasswordAuthentication getPasswordAuthentication() {  
	        return new PasswordAuthentication(user, pwd);  
	    }
	}
}
