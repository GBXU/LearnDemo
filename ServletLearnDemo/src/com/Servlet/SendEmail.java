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
	
	// 上传文件存储目录
    private static final String UPLOAD_DIRECTORY = "upload";
    // 上传配置
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
		// 检测是否为多媒体上传
		if (!ServletFileUpload.isMultipartContent(request)) {
		    // 如果不是则停止
		    PrintWriter writer = response.getWriter();
		    writer.println("Error: 表单必须包含 enctype=multipart/form-data");
			    writer.flush();
			    return;
		}
	    // 配置上传参数
	    DiskFileItemFactory factory = new DiskFileItemFactory();
	    // 设置内存临界值 - 超过后将产生临时文件并存储于临时目录中
	    factory.setSizeThreshold(MEMORY_THRESHOLD);
	    // 设置临时存储目录
	    factory.setRepository(new File(System.getProperty("java.io.tmpdir")));
	    ServletFileUpload upload = new ServletFileUpload(factory);     
	    // 设置最大文件上传值
	    upload.setFileSizeMax(MAX_FILE_SIZE);
	    // 设置最大请求值 (包含文件和表单数据)
	    upload.setSizeMax(MAX_REQUEST_SIZE);
	    // 构造临时路径来存储上传的文件
	    // 这个路径相对当前应用的目录
	    String uploadPath = getServletContext().getRealPath("./") + File.separator + UPLOAD_DIRECTORY;
	    // 如果目录不存在则创建
        File uploadDir = new File(uploadPath);
        if (!uploadDir.exists()) {
            uploadDir.mkdir();
        }
        try {
        @SuppressWarnings("unchecked")// 解析请求的内容提取文件数据
            List<FileItem> formItems = upload.parseRequest(request);
            if (formItems != null && formItems.size() > 0) {
                // 迭代表单数据
	            for (FileItem item : formItems) {
	                // 处理不在表单中的字段
	                if (!item.isFormField()) {
	                    fileName = new File(item.getName()).getName();
	                    filePath = uploadPath + File.separator + fileName;
	                    File storeFile = new File(filePath);
	                    // 在控制台输出文件的上传路径
	                    System.out.println(filePath);
	                    // 保存文件到硬盘
	                    item.write(storeFile);
//	                    request.setAttribute("message",
//	                        "OK");
	                }else {
	                	//因为enctype="multipart/form-data"把表单全部转化为字节流
	                	//所以getParameter()无法正常使用
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
	    // 跳转到 message.jsp
	    //getServletContext().getRequestDispatcher("/message.jsp").forward(request, response);
	    /******************email**********************/
		// 收件人的电子邮件 ID
		String to = "932739864@qq.com";
				//request.getParameter("email");
		// 发件人的电子邮件 ID
		String from = "2014141462281@stu.scu.edu.cn";
		
		
		System.out.println(from_passwd);
		// 假设您是从本地主机发送电子邮件
		String host = "mail.scu.edu.cn";
		// 获取主机的属性
		Properties properties =new Properties();
		properties.setProperty("mail.debug", "true");// 开启debug调试
		properties.setProperty("mail.smtp.auth", "true");// 发送服务器需要身份验证
		properties.setProperty("mail.host", host);// 设置邮件服务器主机名
		properties.setProperty("mail.transport.protocol", "smtp");// 发送邮件协议名称
		// 获取默认的 Session 对象
		Session session = Session.getDefaultInstance(properties,new MyAuthenticator(from,from_passwd));

		// 设置响应内容类型
		response.setContentType("text/html;charset=UTF-8");
		PrintWriter out = response.getWriter();

		try{
			// 创建一个默认的 MimeMessage 对象
			MimeMessage message = new MimeMessage(session);
			// 设置 From: header field of the header.
			message.setFrom(new InternetAddress(from));
			// 设置 To: header field of the header.
			message.addRecipient(Message.RecipientType.TO, new InternetAddress(to));
			// 设置 Subject: header field
			message.setSubject("This is the Subject Line!");
			// 创建消息部分 
			BodyPart messageBodyPart = new MimeBodyPart();
			// 填写消息
			messageBodyPart.setText("This is message body");
 
			// 创建一个多部分消息
			Multipart multipart = new MimeMultipart();
 
			// 设置文本消息部分
			multipart.addBodyPart(messageBodyPart);
 
			// 第二部分是附件
			messageBodyPart = new MimeBodyPart();
			String filename = fileName;
			DataSource source = new FileDataSource(filePath);
			messageBodyPart.setDataHandler(new DataHandler(source));
			messageBodyPart.setFileName(filename);
			multipart.addBodyPart(messageBodyPart);
			
			// 发送完整的消息部分
			message.setContent(multipart );
			
			// 发送消息
			Transport.send(message);
			String title = "发送电子邮件";
			String res = "成功发送电子邮件...";
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
