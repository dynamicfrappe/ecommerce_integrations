frappe.ui.form.on("Item", {
	refresh(frm) {
		if (frm.doc.sync_with_unicommerce) {
			frm.add_custom_button(
				__("Open Unicommerce Item"),
				function () {
					frappe.call({
						method:
							"ecommerce_integrations.unicommerce.utils.get_unicommerce_document_url",
						args: {
							code: frm.doc.item_code,
							doctype: frm.doc.doctype,
						},
						callback: function (r) {
							if (!r.exc) {
								window.open(r.message, "_blank");
							}
						},
					});
				},
				__("Unicommerce")
			);
		}



			frm.add_custom_button(
				__("Syn Item Image"),
				function() {
					frappe.call({
						method:"ecommerce_integrations.shopify.doctype.product_image.send_images_to_shopify" ,
						args :{
							"item_code" :frm.doc.item_code
						}
					})
				},
				__("Image Sync")
			);

	},
});
